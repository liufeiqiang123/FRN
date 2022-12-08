# FRN 
Requirements:

    Python 3 (Anaconda is recommended)
    skimage
    imageio
    Pytorch (Pytorch version >=0.4.1 is recommended)
    tqdm
    pandas
    cv2 (pip install opencv-python)
    Matlab

Test:

    python test.py -opt options/test/test_FRN_x2.json
    python test.py -opt options/test/test_FRN_x3.json
    python test.py -opt options/test/test_FRN_x4.json

    Finally, PSNR/SSIM values for Set5 are shown on your screen, you can find the reconstruction images in ./results
