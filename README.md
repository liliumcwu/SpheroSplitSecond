# SpheroSplitSecond

This project allows you to run four Sphero behaviors using closed loop control: blinking, solid light, fast roll, and slow roll. Designed for an HRI experiment simulating a disaster response scenario, SpheroSplitSecond was developed during the Fall 2018 semester at Yale.

## Getting Started

This project was developed and run on a Windows 8 computer. Note that SpheroNav cannot be run on MacOS 10.11 and above. In order to run the project code, first visit https://github.com/andipeng/SpheroTeam, clone SpheroTeam, and install its necessary dependencies (including the specified fork of the SpheroNav library).

### Prerequisites

No additional dependencies beyond those specified in SpheroTeam's setup.md are necessary.

### Installing

See above.

## Deployment

runLeft.py and runRight.py can be run simultaneously using the run_both.sh script. First connect the Spheros via your computer's bluetooth driver and remember to specify them in the activeBots array. Make sure your Logitech webcam is connected and aimed correctly before running the script.

## Contributing

We based our code on SpheroTeam's notebook #6, which covered camera integration with spheros.

## Authors

* **Lily Wu**
* **Izzy Salinas-Arreola** 

## Context
Developed at Yale University's Scazlab for CPSC 473 Intelligent Robotics Laboratory in Fall 2018, using lab facilities and equipment. We tested our application with the Sphero 2.0 model, running firmware version 3.90+.

## Acknowledgments

* Thanks to Brian Scassellati and Sarah Sebo for their support and advice throughout the duration of this project.
* Additional thanks to our pilot study participants and friends for their support!