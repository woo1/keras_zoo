# Import libraries
import numpy as np
import os
import shutil
import skimage.io as io
import seaborn as sns

# Imports
from skimage.color import label2rgb, rgb2gray, gray2rgb
from skimage import img_as_float
import numpy as np
import scipy.misc


# Converts a label mask to RGB to be shown
def my_label2rgb(labels, colors, bglabel=None, bg_color=(0., 0., 0.)):
    output = np.zeros(labels.shape + (3,), dtype=np.float64)
    for i in range(len(colors)):
        if i != bglabel:
            output[(labels == i).nonzero()] = colors[i]
    if bglabel is not None:
        output[(labels == bglabel).nonzero()] = bg_color
    return output


# Converts a label mask to RGB to be shown and overlaps over an image
def my_label2rgboverlay(labels, colors, image, bglabel=None,
                        bg_color=(0., 0., 0.), alpha=0.2):
    image_float = gray2rgb(img_as_float(rgb2gray(image)))
    label_image = my_label2rgb(labels, colors, bglabel=bglabel,
                               bg_color=bg_color)
    output = image_float * alpha + label_image * (1 - alpha)
    return output


# Save image
def save_img(img, mask, fname, color_map, void_label):
    img = img / 255.

    label_mask = my_label2rgboverlay(mask,
                                     colors=color_map,
                                     image=img,
                                     bglabel=void_label,
                                     alpha=0.2)

    combined_image = np.concatenate((img, label_mask), axis=1)
    scipy.misc.toimage(combined_image).save(fname)


# Create the output paths
def create_paths(path, set):
    # Create a folder
    def makedir(path):
        if not os.path.exists(path):
            os.makedirs(path)

    # Create path names
    path_set = os.path.join(path, set)
    path_set_images = os.path.join(path_set, "images")
    path_set_gt = os.path.join(path_set, "masks")

    # Create folders
    makedir(path)
    makedir(path_set)
    makedir(path_set_images)
    makedir(path_set_gt+'2')
    makedir(path_set_gt+'3')
    makedir(path_set_gt+'4')

    # Return folder names
    return path_set, path_set_images, path_set_gt


# Main function
def main(dataset_path, dataset_path2, new_dataset_path, n_classes=4):
    # Get paths
    images_path = dataset_path + 'images/'
    images_path2_cvc300 = os.path.join(dataset_path2, 'CVC-300/bbdd/')
    images_path2_cvc612 = os.path.join(dataset_path2, 'CVC-612/bbdd/')
    masks_path2_cvc300 = os.path.join(dataset_path2, 'CVC-300/')
    masks_path2_cvc612 = os.path.join(dataset_path2, 'CVC-612/')
    new_images_path = os.path.join(new_dataset_path, 'images/')
    new_masks_path = os.path.join(new_dataset_path, 'masks')

    # Get testing files
    file_names = os.listdir(images_path)

    unique_mask_2 = []
    unique_mask_3 = []
    unique_mask_4 = []
    # Process each file
    for name in file_names:
        print (name)
        # Get dataset and file name
        dataset = name[0:7]
        file_raw = name[:-4]
        file_int = int(name[8:-4])

        # Get input image and mask names
        img_name = images_path + name
        if dataset == 'CVC-300':
            mask_name_2 = masks_path2_cvc300 + 'labelled2classes/' + str(file_int) + '.tif'
            mask_name_3 = masks_path2_cvc300 + 'labelled3classes/' + str(file_int) + '.tif'
            mask_name_4 = masks_path2_cvc300 + 'labelled4classes/' + str(file_int) + '.tif'
        else:
            mask_name_2 = masks_path2_cvc612 + 'labelled2classes/' + str(file_int) + '.tif'
            mask_name_3 = masks_path2_cvc612 + 'labelled3classes/' + str(file_int) + '.tif'
            mask_name_4 = masks_path2_cvc612 + 'labelled4classes/' + str(file_int) + '.tif'
        # print ('Image name: ' + str(img_name))
        # print ('Mask name 3: ' + str(mask_name_3))
        # print ('Mask name 4: ' + str(mask_name_4))

        # Load image and mask
        image = io.imread(img_name)

        # 4 Classes
        mask_4 = io.imread(mask_name_4)
        mask_4 = mask_4.astype('int32')

        # 3 Classes
        mask_3 = io.imread(mask_name_3)
        mask_3 = mask_3.astype('int32')

        # 2 Classes
        mask_2 = io.imread(mask_name_2)
        mask_2 = mask_2.astype('int32')

        unique_2 = np.unique(mask_2)
        unique_3 = np.unique(mask_3)
        unique_4 = np.unique(mask_4)
        unique_mask_2 = np.unique(np.concatenate((unique_mask_2, unique_2)))
        unique_mask_3 = np.unique(np.concatenate((unique_mask_3, unique_3)))
        unique_mask_4 = np.unique(np.concatenate((unique_mask_4, unique_4)))
        # print ('Mask 2 unique: ' + str(unique_2))
        # print ('Mask 3 unique: ' + str(unique_3))
        # print ('Mask 4 unique: ' + str(unique_4))
        # print ('Mask 2 unique final: ' + str(unique_mask_2))
        # print ('Mask 3 unique final: ' + str(unique_mask_3))
        # print ('Mask 4 unique final: ' + str(unique_mask_4))

        # Get input image and mask names
        out_img_name = new_images_path + file_raw + '.bmp'
        out_mask_name_2 = new_masks_path + '2/' + file_raw + '.tif'
        out_mask_name_3 = new_masks_path + '3/' + file_raw + '.tif'
        out_mask_name_4 = new_masks_path + '4/' + file_raw + '.tif'
        # print ('Out Image name: ' + str(out_img_name))
        # print ('Out Mask name 2: ' + str(out_mask_name_2))
        # print ('Out Mask name 3: ' + str(out_mask_name_3))
        # print ('Out Mask name 4: ' + str(out_mask_name_4))

        # Copy the files
        shutil.copy(img_name, out_img_name)
        shutil.copy(mask_name_2, out_mask_name_2)
        shutil.copy(mask_name_3, out_mask_name_3)
        shutil.copy(mask_name_4, out_mask_name_4)

        # Copy the files
        # shutil.copy(img_name, out_img_name)
        # io.imsave(out_img_name, image)
        # io.imsave(out_mask_name_2, mask_2)
        # io.imsave(out_mask_name_3, mask_3)
        # io.imsave(out_mask_name_4, mask_4)
        # exit()

        # # Show result
        # # color_map = sns.hls_palette(7)
        # # print ("Color palete: " + str(color_map))
        # color_map = [
        #     (255/255., 0, 0),                   # Background
        #     (192/255., 192/255., 128/255.),     # Polyp
        #     (128/255., 64/255., 128/255.),      # Lumen
        #     (0, 0, 255/255.),                   # Specularity
        #     (0, 255/255., 0),         #
        #     (192/255., 128/255., 128/255.),     #
        #     (64/255., 64/255., 128/255.),       #
        # ]
        # # print ("Color palete2: " + str(color_map))
        # out_res_2 = new_masks_path + '2/res_' + file_raw + '.png'
        # out_res_3 = new_masks_path + '3/res_' + file_raw + '.png'
        # out_res_4 = new_masks_path + '4/res_' + file_raw + '.png'
        # save_img(image, mask_2, out_res_2, color_map, 2)
        # save_img(image, mask_3, out_res_3, color_map, 3)
        # save_img(image, mask_4, out_res_4, color_map, 4)
        # # exit()


# Entry point of the script
if __name__ == '__main__':

    # Create the folders
    print ('> Creating output folders...')
    out_path = '/data/lisa/exp/vazquezd/datasets/polyps_split7/'
    path1 = '/data/lisa/exp/vazquezd/datasets/polyps_split2/CVC-912/'
    path2 = '/data/lisa/exp/vazquezd/datasets/polyps_NewGT4/'
    path_train, path_train_images, path_train_gt = create_paths(out_path, "train")
    path_valid, path_valid_images, path_valid_gt = create_paths(out_path, "valid")
    path_test, path_test_images, path_test_gt = create_paths(out_path, "test")

    print ('Train...')
    main(dataset_path=path1 + 'train/',
         dataset_path2=path2,
         new_dataset_path=path_train)

    print ('Valid...')
    main(dataset_path=path1 + 'valid/',
         dataset_path2=path2,
         new_dataset_path=path_valid)

    print ('Test...')
    main(dataset_path=path1 + 'test/',
         dataset_path2=path2,
         new_dataset_path=path_test)