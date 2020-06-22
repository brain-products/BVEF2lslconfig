# Overview

This python utility is for injecting channel label data from a .bvef (BrainVision Electrode Format) file to an existing lsl-style .cfg configuration file. To use, you must have python installed on your computer. You will need to point to the location of this script with your [`[PYTHONPATH]` environment variable](https://docs.python.org/3/using/cmdline.html#environment-variables). Then from a command prompt navigate to the folder with desired files and type (for example): 
  ```
  python BVEF2lslconfig.py RNP-LA-32.bvef liveamp32_config_ini.cfg
  ```
The output file will have the name of these two files concatenated (liveamp32_config_ini-RNP-LA_32.cfg). More bvef files are available from the [Brain Products website](https://www.brainproducts.com/downloads.php?kid=44). 

If you wish to convert an older, XML formated config file, you may do so by adding the flag XML to the argument list:
  ```
  python BVEF2lslconfig.py RNP-LA-32.bvef liveamp32_config_xml.cfg XML
  ```
This was tested against python 2.7 and 3.7.
