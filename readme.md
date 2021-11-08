# Components of a warning system for cyclists

This repository contains components for a system that uses computer vision and tinyML to warn cyclists of vehicles approaching from behind in order to increase their safety. 

For this, mobileNets of different versions and variants were trained using transfer learning with image and thermal image (sensor: MLX90640) data sets collected specifically for this purpose.

In `models` trained and quantized as well as non-quantized variants can be found.  

These can be deployed on an OpenMV Cam H7 (Plus) as follows:
- Connect MLX90640 via I²C
- Connect OpenMV Cam (with inserted SD card) with the OpenMV IDE. Please note that for most models an OpenMV Cam H7 Plus is required.
- Open `prototype.py` in OpenMV IDE and save it on the connected OpenMV Cam as `main.py`.
- Select models (cam and mlx) and save them on the OpenMV Cam. Note that v1- and v3-models may not work due to unsupported layers.
- Create folders "cam" and "mlx" on OpenMV Cam

The script currently logs the predictions of the deployed models. A next step would be to connect a suitable warning signal.  

-  `openmv/datalogger.py` was used on a OpenMV Cam H7 to collect the dataset.
-  `scripts/data-labeling.py` was used to label the collected dataset.
-  `scripts/mobileNet_transfer_learning.ipynb` is the script that was used to train the models.
