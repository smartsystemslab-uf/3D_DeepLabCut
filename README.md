# 3D_DeepLabCut
## deeplabcut_project
This folder contains different DeepLabCut projects used for testing. The most recent project where development occurred in the **dev** directory was **uf_cobots_multicam-Derek_Perdomo-2023-06-12**.

## dev 
This folder contains the development files. Here, the **main.py** can be used to give an example of how to read the files located in **frame_data**. Within **frame_data**, there a 3 pickle data files containing lists of Frame objects without bounding box data and 3 pickle data files containing bounding box data. Those with the bounding box data are appended with **_bb**. Additionally, each pickle file references a specific camera where camera 1 is the -45 degrees, camera 2 is 0 degrees, and camera 3 is 45 degrees relative to camera 2. Lastly, the architecture for the Frame objects can be found in **data_types.py**.

## env_docker
This folder contains the python environment used for using docker for DeepLabCut.

## Specs:
OS: Ubuntu 18.04

### deeplabcut_projects
These were run using the env_docker environment.

### development
Python Version: 3.8.0
