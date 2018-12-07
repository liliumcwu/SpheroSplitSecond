# SpheroSplitSecond

This project allows you to run four Sphero behaviors using closed loop control: blinking, solid light, fast roll, and slow roll. Designed for an HRI experiment simulating a disaster response scenario, SpheroSplitSecond was developed during the Fall 2018 semester at Yale.

## Getting Started

This project was developed and run on a Windows 8 computer. Note that SpheroNav cannot be run on MacOS 10.11 and above. In order to run the project code, first visit https://github.com/andipeng/SpheroTeam, clone SpheroTeam, and install its necessary dependencies (including the specified fork of the SpheroNav library).

### Prerequisites

No additional dependencies beyond those specified in SpheroTeam's setup.md are necessary. Note that you don't specifically need version 2.4 of Open CV.

### Setup

In SpheroNAV folder → tracker → trackerbase.py 
* If using camera connected to laptop via USB port, for lines 37 & 103
  * Change ```cameraID = -1``` to ```cameraID = 1```
* Change line 45
  * ```self.image_size = (int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)))```
* Add ```__,``` to beginning of line 71 so it reads
  * ```__, countours, hierarchy = cv2.findCountours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)```
* In SpheroTEAM, replace their requirements.txt with ours
* Our version has removed:
  * nb-anacondacloud
  * nb-conda
  * nb-conda-kernels
  * nbpresent 
  * pywin32
  * tables 
* You will most likely need to install (if conda install does not work, use pip install and vice versa):
  * conda install anaconda-clean
  * conda install anaconda-client
  * conda install anaconda-navigator
  * conda install colour
  * pip install comtypes
  * conda install conda-build
  * pip install menuinst or conda install menuinst 
  * pip install open-cv python
  * conda install ruamel-yaml
  * pip install openpyxl
  * pip install path.py
* If you are running windows 8: 
  * pybluez might not be able to find your Windows SDK directory
  * Download Windows SDK here (do not download C++ first): https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk  
  * In the pybluez setup.py file inside the function ```find_MS_SDK()``` line 39
    * In lines 53, 56, and 59 change to ```candidate_paths```


## Deployment

runLeft.py and runRight.py can be run simultaneously using the run_both.sh script. First connect the Spheros via your computer's bluetooth driver and remember to specify them in the activeBots array. Make sure your Logitech webcam is connected and aimed correctly before running the script.

## Contributing

We based our code on SpheroTeam's notebook #6, which covered camera integration with spheros.

## Authors

* **Lily Wu**
* **Isabel Salinas-Arreola** 

## Context
Developed at Yale University's Scazlab for CPSC 473 Intelligent Robotics Laboratory in Fall 2018, using lab facilities and equipment. We tested our application with the Sphero 2.0 model, running firmware version 3.90+.

## Acknowledgments

* Thanks to Brian Scassellati and Sarah Sebo for their support and advice throughout the duration of this project.
* Additional thanks to our pilot study participants and friends for their support!