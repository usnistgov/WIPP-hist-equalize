# NIST-developed software is provided by NIST as a public service. You may use, copy and distribute copies of the software in any medium, provided that you keep intact this entire notice. You may improve, modify and create derivative works of the software or any portion of the software, and you may copy and distribute such modifications or works. Modified works should carry a notice stating that you changed the software and should note the date and nature of any such change. Please explicitly acknowledge the National Institute of Standards and Technology as the source of the software.
# NIST-developed software is expressly provided "AS IS." NIST MAKES NO WARRANTY OF ANY KIND, EXPRESS, IMPLIED, IN FACT OR ARISING BY OPERATION OF LAW, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT AND DATA ACCURACY. NIST NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE OR THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY, RELIABILITY, OR USEFULNESS OF THE SOFTWARE.
# You are solely responsible for determining the appropriateness of using and distributing the software and you assume all risks associated with its use, including but not limited to the risks and costs of program errors, compliance with applicable laws, damage to or loss of data, programs or equipment, and the unavailability or interruption of operation. This software is not intended to be used in any situation where a failure could cause risk of injury or damage to property. The software developed by NIST employees is not subject to copyright protection within the United States.

import os
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt # this is for debugging

'''
the method for applying image histogram equalization to one image
code inspired by https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html
It support 8 BPP and 16 BPP images
Note: RGB images are converted to grayscale and then enhanced

individual steps are described at
https://levelup.gitconnected.com/introduction-to-histogram-equalization-for-digital-image-enhancement-420696db9e43
Published methods have been extended to work on 16 BPP images
'''
def hist_equal(img_file, input_dir, output_dir):
    img_filename = os.path.join(input_dir, img_file)
    save_filename = os.path.join(output_dir, img_file)
    img = cv.imread(img_filename, cv.IMREAD_UNCHANGED) #  cv.IMREAD_ANYDEPTH; cv.IMREAD_UNCHANGED - Read Image with Transparency Channel
    print('Image size:', img.size)
    print(f'dtype: {img.dtype}, shape: {img.shape}, min: {np.min(img)}, max: {np.max(img)}')

    if img.dtype != 'uint8' and img.dtype != 'uint16':
        print('ERROR: unsupported input image format')
        return

    equ = None
    # grayscale/single channel support
    if len(img.shape) < 3: # contains #rows and #cols
        if img.dtype == 'uint8':
            # the case of 8BPP
            equ = cv.equalizeHist(img) #works only for 8BPP
            # hist, bins = np.histogram(img.flatten(), 256, [0, 256])
            # cdf = hist.cumsum()
            # cdf_normalized = cdf * float(hist.max()) / cdf.max()
            # # plt.plot(cdf_normalized, color='b')
            # # plt.hist(img.flatten(), 256, [0, 256], color='r')
            # # plt.xlim([0, 256])
            # # plt.legend(('cdf', 'histogram'), loc='upper left')
            # # plt.show()
            # # Now we have the look-up table...
            # equ = cdf_normalized[img]

        if img.dtype == 'uint16':
            # the case of 16 BPP
            hist, bins = np.histogram(img.flatten(), 65536, [0, 65536])  # Collect 16 bits histogram (65536 = 2^16).
            cdf = hist.cumsum()
            cdf_m = np.ma.masked_equal(cdf, 0)  # Find the minimum histogram value (excluding 0)
            cdf_m = (cdf_m - cdf_m.min()) * 65535 / (cdf_m.max() - cdf_m.min())
            cdf = np.ma.filled(cdf_m, 0).astype('uint16')
            # Now we have the look-up table...
            equ = cdf[img]
    elif len(img.shape) == 3:
        # width = img.shape[0]
        # height = img.shape[1]
        # channels = img.shape[2]
        # print('INFO: width=', width, ' height=', height, ' channels=', channels)

        # color/3 channel support
        if img.dtype == 'uint8':
            # the case of 8BPP
            hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            ##### debug
            # save_filename2 = os.path.join(output_dir, str('debugHSV_'+img_file))
            # cv.imwrite(save_filename2, hsv_img)
            # rgb_img = cv.cvtColor(hsv_img, cv.COLOR_HSV2BGR) # cv.COLOR_HSV2RGB; cv.COLOR_HSV2BGR
            # save_filename3 = os.path.join(output_dir, str('debugRGB_'+img_file))
            # cv.imwrite(save_filename3, rgb_img)

            v_img = hsv_img[:, :, 2]
            # save_filename4 = os.path.join(output_dir, str('debugHvalue_'+img_file))
            # cv.imwrite(save_filename4, v_img)

            v_equ = cv.equalizeHist(v_img)  # works only for 8BPP
            # save_filename5 = os.path.join(output_dir, str('debugHvalueEQU_'+img_file))
            # cv.imwrite(save_filename5, v_equ)

            hsv_img[:,:, 2] = v_equ;
            equ = cv.cvtColor(hsv_img, cv.COLOR_HSV2BGR) # cv.COLOR_HSV2RGB; cv.COLOR_HSV2BGR

    else:
        print('ERROR: unsupported number of channels')
        return

    cv.imwrite(save_filename, equ)

'''
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
# https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html
This method introduces some artifacts although it might be helpful when parts 
of an image are saturated.
Note: the 8BPP vs 16BPP versions might need separate treatments (and hence are separated)
'''
def hist_equal_CLAHE(img_file, input_dir, output_dir):
    img_filename = os.path.join(input_dir, img_file)
    save_filename = os.path.join(output_dir, img_file)
    img = cv.imread(img_filename, cv.IMREAD_ANYDEPTH)
    print('INFO: img type =', img.dtype)

    equ = None
    if img.dtype == 'uint8':
        # the case of 8BPP
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equ = clahe.apply(img)

    if img.dtype == 'uint16':
        # the case of 16 BPP
        clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        equ = clahe.apply(img)

    if img.dtype != 'uint8' and img.dtype != 'uint16':
        print('ERROR: unsupported input image format')
        return

    cv.imwrite(save_filename, equ)



def main():
    import argparse
    # Setup the Argument parsing
    parser = argparse.ArgumentParser(prog='apply histogram equalization to input images in a folder',
                                     description='Script which takes input: folder with images, folder for output images')
    parser.add_argument('--inputImages', dest='input_dir', type=str,
                        help='directory with tif image files (Required)', required=True)
    parser.add_argument('--output', dest='output_dir', type=str,
                        help='output directory where updated image files are saved (Required)', required=True)
    parser.add_argument('--suffix', dest='image_suffix', type=str,
                        help='image file suffix in the input directory (Optional)', required=False, default=None)


    args = parser.parse_args()
    if args.input_dir is None:
        print('ERROR: missing input_dir ')
        return

    if args.output_dir is None:
        print('ERROR: missing output_dir ')
        return

    input_dir = args.input_dir
    output_dir = args.output_dir

    image_suffix = '.tif'
    if args.image_suffix is not None:
        image_suffix = args.image_suffix

    print('Arguments:')
    print('input input_dir = {}'.format(input_dir))
    print('input image_suffix = {}'.format(image_suffix))
    print('output_dir = {}'.format(output_dir))

    # sanity checks
    if not os.path.isdir(output_dir):
        # make directory if needed
        try:
            os.mkdir(output_dir)
        except OSError as error:
            print(error)

    # sanity check
    if not os.path.isdir(input_dir):
        print('ERROR: input_dir=', input_dir, ' is not a directory')
        return


    file_list = []
    for t_file in os.listdir(input_dir):
        # check for only files with the expected suffix
        if os.path.isfile(os.path.join(input_dir, t_file)) and t_file.endswith(image_suffix):
            file_list.append(t_file)
    print('INFO: file_list=', file_list)
    if len(file_list) < 1:
        print('WARNING: input dir=', input_dir,
              ' does not contain any files with suffix:', image_suffix)
        return

    print('INFO: list of files =', file_list)
    for file_name in file_list:
        # hist_eq(file_name, input_dir, output_dir)
        # hist_equal_CLAHE(file_name, input_dir, output_dir)
        hist_equal(file_name, input_dir, output_dir)


if __name__ == "__main__":
    main()
