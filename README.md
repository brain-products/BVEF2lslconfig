Overview
###########

This python utility is for injecting channel label data from a .bvef (BrainVision Electrode Format) file to an existing lsl-style .cfg configuration file. To use, you must have python installed on your computer. Then from a command prompt navigate to the folder with desired files and type (for example): 

python RNP-LA-32.bvef liveamp32_config.cfg

The output file will have the name of these two files concatenated. More bvef files are available from the [Brain Products website] (https://www.brainproducts.com/downloads.php?kid=44 "Brain Products website"). This was tested against python 2.7 and 3.7.
