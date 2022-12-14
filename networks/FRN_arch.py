import torch
import torch.nn as nn
from .blocks import MeanShift

#shadow module
class shadow_module(nn.Module):
    def __init__(self, num_features):
        super(shadow_module, self).__init__()

        hidchannels = num_features//2

        self.conv1 = nn.Sequential(*[
            nn.Conv2d(in_channels=num_features, out_channels=hidchannels, kernel_size=3, padding=1, stride=1),
            nn.LeakyReLU()
        ])

        self.conv2 = nn.Sequential(*[
            nn.Conv2d(in_channels=hidchannels, out_channels=hidchannels, kernel_size=3, padding=1,stride=1,groups=hidchannels),
            nn.LeakyReLU()
        ])

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv2(x1)
        out = torch.cat([x1, x2], dim=1)
        return out

#Channel Attention (CA) Layer
class CALayer(nn.Module):
    def __init__(self, channel, reduction=16):
        super(CALayer, self).__init__()
        # global average pooling: feature --> point
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        # feature channel downscale and upscale --> channel weight
        self.conv_du = nn.Sequential(
                nn.Conv2d(channel, channel // reduction, 1, padding=0, bias=True),
                nn.ReLU(inplace=True),
                nn.Conv2d(channel // reduction, channel, 1, padding=0, bias=True),
                nn.Sigmoid()
        )

    def forward(self, x):
        y = self.avg_pool(x)
        y = self.conv_du(y)
        return x * y

#Feature Refined Block (FRB)
class FRB(nn.Module):
    def __init__(self, num_features):
        super(FRB, self).__init__()

        self.c1 = nn.Sequential(*[
            shadow_module(num_features=num_features),
            nn.LeakyReLU()
        ])
        self.c2 = nn.Sequential(*[
            shadow_module(num_features=num_features),
            nn.LeakyReLU()
        ])
        self.c3 = nn.Sequential(*[
            shadow_module(num_features=num_features),
            nn.LeakyReLU()
        ])
        self.c4 = nn.Sequential(*[
            shadow_module(num_features=num_features),
            nn.LeakyReLU()
        ])

        self.cat1 = nn.Sequential(*[
            nn.Conv2d(in_channels=2 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])
        self.cat2 = nn.Sequential(*[
            nn.Conv2d(in_channels=3 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])
        self.cat3 = nn.Sequential(*[
            nn.Conv2d(in_channels=4 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])
        self.cat4 = nn.Sequential(*[
            nn.Conv2d(in_channels=5 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])
        
        #Channel attention
        self.CA = CALayer(num_features)

    def forward(self,x):
        f1 = self.c1(x)
        f11 = self.cat1(torch.cat((x, f1), dim=1))

        f2 = self.c2(f11)
        f22 = self.cat2(torch.cat((x, f1, f2), dim=1))

        f3 = self.c3(f22)
        f33 = self.cat3(torch.cat((x, f1, f2, f3), dim=1))

        f4 = self.c4(f33)
        f44 = self.cat4(torch.cat((x, f1, f2, f3, f4), dim=1))

        f5 = self.CA(f44)
        return x + f5

#Feature Refined network (FRN)
class FRN(nn.Module):
    def __init__(self, in_channels, out_channels, num_features, upscale_factor):
        super(FRN, self).__init__()

        self.upscale_factor = upscale_factor

        # RGB mean for DIV2K
        rgb_mean = (0.4488, 0.4371, 0.4040)
        rgb_std = (1.0, 1.0, 1.0)
        self.sub_mean = MeanShift(rgb_mean, rgb_std)

        # initial low-level feature extraction block
        self.head = nn.Sequential(*[
            nn.Conv2d(in_channels=in_channels, out_channels=num_features,kernel_size=3,padding=1,stride=1)
        ])

        self.block1 = FRB(num_features)
        self.block2 = FRB(num_features)
        self.block3 = FRB(num_features)
        self.block4 = FRB(num_features)
        self.block5 = FRB(num_features)

        self.cat1 = nn.Sequential(*[
            nn.Conv2d(in_channels=2 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])

        self.cat2 = nn.Sequential(*[
            nn.Conv2d(in_channels=3 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])

        self.cat3 = nn.Sequential(*[
            nn.Conv2d(in_channels=4 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])

        self.cat4 = nn.Sequential(*[
            nn.Conv2d(in_channels=5 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])

        self.cat5 = nn.Sequential(*[
            nn.Conv2d(in_channels=6 * num_features, out_channels=num_features, kernel_size=1, padding=0, stride=1),
            nn.LeakyReLU()
        ])

        if upscale_factor == 2 or upscale_factor == 3:
            self.UPNet = nn.Sequential(*[
                nn.Conv2d(num_features, out_channels * upscale_factor* upscale_factor, kernel_size=3, padding=1,stride=1),
                nn.PixelShuffle(upscale_factor)
            ])
        elif upscale_factor == 4:
            self.UPNet = nn.Sequential(*[
                nn.Conv2d(num_features, out_channels * upscale_factor* upscale_factor, kernel_size=3, padding=1,stride=1),
                nn.PixelShuffle(4)
            ])
        else:
            raise ValueError("upscale_factor must be 2,3,4.")

        self.add_mean = MeanShift(rgb_mean, rgb_std, 1)

    def forward(self, x):
        x = self.sub_mean(x)
        inter_res = nn.functional.interpolate(x, scale_factor=self.upscale_factor, mode='bilinear', align_corners=False)
        fea = self.head(x)

        x1 = self.block1(fea)
        x11 = self.cat1(torch.cat((fea, x1),dim=1))

        x2 = self.block2(x11)
        x22 = self.cat2(torch.cat((fea, x1, x2),dim=1))

        x3 = self.block3(x22)
        x33 = self.cat3(torch.cat((fea, x1, x2, x3),dim=1))

        x4 = self.block4(x33)
        x44 = self.cat4(torch.cat((fea, x1, x2, x3, x4),dim=1))

        x5 = self.block5(x44)
        x55 = self.cat5(torch.cat((fea, x1, x2, x3, x4, x5), dim=1))

        out = self.UPNet(x55) + inter_res
        h = self.add_mean(out)
        return h
      
