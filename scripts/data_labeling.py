from natsort import natsorted
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import pandas as pd

pd.options.mode.chained_assignment = None

# Folder containing the collected datasets
path_beginning = "data/"

current_data_folder = "2021-06-03/"

# temperature log
path_mlx_temp = path_beginning + current_data_folder + "mlxTemp.txt"
path_mlx_temp_labelled = path_beginning + current_data_folder + "mlxTemp_labelled.csv"

# normal camera
path_labelled_warn_cam = path_beginning + current_data_folder + "cam_labelled/warn/"
path_labelled_not_warn_cam = path_beginning + current_data_folder + "cam_labelled/not_warn/"
path_labelled_not_warn_car_cam = path_beginning + current_data_folder + "cam_labelled/not_warn_car/"
path_source_cam_images = path_beginning + current_data_folder + "cam/"

# mlx90640 sensor
path_labelled_warn_mlx = path_beginning + current_data_folder + "mlx_labelled/warn/"
path_labelled_not_warn_mlx = path_beginning + current_data_folder + "mlx_labelled/not_warn/"
path_labelled_not_warn_car_mlx = path_beginning + current_data_folder + "mlx_labelled/not_warn_car/"
path_source_mlx_images = path_beginning + current_data_folder + "mlx/"

path_labelled_deleted = path_beginning + current_data_folder + "deleted/"

# loading images
def load_images_from_folder(folder):
    images = {} # dict with file name as key and jpg as value
    for filename in os.listdir(folder):
        img = mpimg.imread(os.path.join(folder,filename))
        if img is not None:
            #remove first 3 and last 4 characters from string:
            filename = filename[4:-4]
            images[filename] = img
    return images

# load images
cam_images = load_images_from_folder(path_source_cam_images)

# load temperature log as a pandas dataframe
mlx_temp = pd.read_csv(path_mlx_temp, sep=";")

# Show each image with dangerous area drawn in and label them based on the input
for img_key in natsorted(cam_images):
    plt.imshow(cam_images[img_key])

    # dangerous area
    point1 = [167, 238]
    point2 = [169, 116]
    point3 = [280, 111]
    point4 = [319, 132]
    x_values = [point1[0], point2[0], point3[0], point4[0]]
    y_values = [point1[1], point2[1], point3[1], point4[1]]

    plt.plot(x_values, y_values, 'c')
    plt.title(img_key)

    plt.pause(0.05)

    label_raw = input()

    filename_cam = "cam_" + img_key + ".jpg"
    filename_mlx = "mlx_" + img_key + ".jpg"
    print(img_key)
    source_path_cam = path_source_cam_images + filename_cam
    source_path_mlx = path_source_mlx_images + filename_mlx
    mlx_temp_row = mlx_temp[mlx_temp['key'] == int(img_key)]


    if label_raw == "w":        
        target_path_cam = path_labelled_warn_cam + filename_cam
        target_path_mlx = path_labelled_warn_mlx + filename_mlx
        mlx_temp_row['label'] = "warn"
    elif label_raw == "c":
        target_path_cam = path_labelled_not_warn_car_cam + filename_cam
        target_path_mlx = path_labelled_not_warn_car_mlx + filename_mlx
        mlx_temp_row['label'] = "not_warn_car"
    elif label_raw == "d":
        target_path_cam = path_labelled_deleted + filename_cam
        target_path_mlx = path_labelled_deleted + filename_mlx
        mlx_temp_row['label'] = "deleted"
    else:
        target_path_cam = path_labelled_not_warn_cam + filename_cam
        target_path_mlx = path_labelled_not_warn_mlx + filename_mlx
        mlx_temp_row['label'] = "not_warn"

    print(mlx_temp_row)

    # replace camera files
    os.replace(source_path_cam, target_path_cam)

    # replace mlx files
    os.replace(source_path_mlx, target_path_mlx)

    # if file does not exist write header 
    if not os.path.isfile(path_mlx_temp_labelled):
        mlx_temp_row.to_csv(path_mlx_temp_labelled, header='column_names', sep=';', index = False)
    else: # else it exists so append without writing the header
        mlx_temp_row.to_csv(path_mlx_temp_labelled, mode='a', header=False, sep=';', index = False)

    plt.close()