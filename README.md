# SkinFairHAM
The published code for the master thesis "Towards equitable deep learning in dermatology: Assessing lesion classification fairness across skin tones".


To reproduce the experiments the ISIC 2018 Task 3 training data needs to be downloaded from https://challenge.isic-archive.com/data/#2018  and saved in ./data/ISIC2018/ISIC2018_Task3_Training_Input/.

To fully reproduce the experiments, one would need the ITA labels, which are proprietary to IBM and cannot be published. Also the provided segmentation model, which was assessed cannot be published. The ITA labels would be found in ./data/ISIC2018/ISIC2018_Task3_Training_Input/metadata.csv in the "estimated_ita" column. However, the test sets' image names for each experiment are provided in the csv of the predictions folder, which allows for the ligth-dark test split.

The SINGAN repository can be pulled from https://github.com/tamarott/SinGAN. The training images are provided in the Input subfolder. Note that the SINGAN repository has its own requirements and should be run in its own environment.
