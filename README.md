# DepthAI-GUI

**This repository is a fork of PyFlow tool, to learn more about it, please [click here to go to the original repository](https://github.com/wonderworks-software/PyFlow)**

DepthAI GUI is a WYSIWYG tool that allows to create a custom DepthAI pipelines, run them and see the results - all
in one tool.

It's purpose is to allow users to create computer vision prototypes quickly, focusing on **what** rather than **how**

## Demo


[![Gaze Example Demo](https://user-images.githubusercontent.com/5244214/102778186-6729a200-4392-11eb-981a-b2f3db50c2b9.gif)](https://www.youtube.com/watch?v=yNFgp1xrE80)


## Install 

```
pip install --extra-index-url https://artifacts.luxonis.com/artifactory/luxonis-python-snapshot-local/ depthai-gui
```

## Usage

To start the GUI, run

```
depthai-gui
```

To run a specific example (`example.pygraph`) run

```
depthai-gui -f /path/to/example.pygraph
```

## Troubleshooting

### AttributeError: module 'Qt' has no attribute 'QtGui'

We experienced this issue with Qt library on Ubuntu 18.04, and the cause of this error was in missing libraries.

To make it work, please make sure you have the following libraries installed:

```
sudo apt-get install libgl1-mesa-glx libpulse-dev libxcb-xinerama0 libfontconfig libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xkb1 libxkbcommon-x11-0
```

[Here](https://gist.github.com/VanDavv/62d1940f83fe2059f4734a5a7b40caf7) is a gist showing a working Ubuntu 18.04 example
installation based on Docker.