# FRN 
Requirements:

    1. Python==3.6 (Anaconda is recommended)
    2. skimage
    3. imageio
    4. Pytorch==1.2
    5. tqdm
    6. pandas
    7. cv2 (pip install opencv-python)
    8. Matlab

Test:

    python test.py -opt options/test/test_FRN_x2.json
    python test.py -opt options/test/test_FRN_x3.json
    python test.py -opt options/test/test_FRN_x4.json

    Finally, PSNR/SSIM values for Set5 are shown on your screen, you can find the reconstruction images in ./results. Other standard SR benchmark dadasets, you need to
    change the datasets storage path in the test_FRN_x2.json, test_FRN_x3.json and test_FRN_x4.json files.
    
    
If you find our work useful in your research or publications, please consider citing:

    @article{liu2022lightweight,
      title={Lightweight image super-resolution with a feature-refined network},
      author={Liu, Feiqiang and Yang, Xiaomin and De Baets, Bernard},
      journal={Signal Processing: Image Communication},
      pages={116898},
      year={2022},
      publisher={Elsevier}
    }
