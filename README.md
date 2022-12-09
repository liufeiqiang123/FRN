# Lightweight Image Super-Resolution with a Feature-Reﬁned Network
This repository is Pytorch code for our proposed FRN.
![figure2](https://user-images.githubusercontent.com/42378133/206620532-d68ae121-b41b-4bd1-9e3f-240052fe303b.png)
Schematic representation of the proposed Feature-Reﬁned Network (FRN) and its submodules. The details about our proposed FRN can be found in our main paper:https://www.sciencedirect.com/science/article/pii/S0923596522001771.

If you find our work useful in your research or publications, please star the code and consider citing:

    @article{liu2022lightweight,
      title={Lightweight image super-resolution with a feature-refined network},
      author={Liu, Feiqiang and Yang, Xiaomin and De Baets, Bernard},
      journal={Signal Processing: Image Communication},
      pages={116898},
      year={2022},
      publisher={Elsevier}
    }

## Requirements:

    1. Python==3.6 (Anaconda is recommended)
    2. skimage
    3. imageio
    4. Pytorch==1.2
    5. tqdm
    6. pandas
    7. cv2 (pip install opencv-python)
    8. Matlab

## Test:

    python test.py -opt options/test/test_FRN_x2.json
    python test.py -opt options/test/test_FRN_x3.json
    python test.py -opt options/test/test_FRN_x4.json

    Finally, PSNR/SSIM values for Set5 are shown on your screen, you can find the reconstruction images in ./results. Other standard SR benchmark dadasets, you need to
    change the datasets storage path in the test_FRN_x2.json, test_FRN_x3.json and test_FRN_x4.json files.
    
## Results:

Quantitative Results:
![Quantitative Results](https://user-images.githubusercontent.com/42378133/206619675-b21e628b-1393-4d99-b415-96b56a594c5e.png)
Average PSNR/SSIM for x2, x3 and x4 SR on datasets Set5, Set14, B100, Urban100, and Manga109. The best and second best results are highlighted in
red and blue, respectively.

Some Qualitative Results:
![figure5](https://user-images.githubusercontent.com/42378133/206620012-87495f7a-66c2-4cfd-8f39-42dc425a2e05.png)
Visual comparison of the results of our FRN with those of other state-of-the-art lightweight methods on some images from the B100 and Urban100
datasets for x4 SR. The best results are indicated in bold.
