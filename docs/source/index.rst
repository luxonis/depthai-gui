.. Luxonis Docs documentation master file, created by
   sphinx-quickstart on Tue Nov  3 14:34:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DepthAI GUI documentation
=========================

DepthAI GUI is a WYSIWYG tool that allows to create a custom DepthAI
pipelines, run them and see the results - all
in one tool.

It's purpose is to allow users to create computer vision prototypes
quickly, focusing on **what** rather than **how**

Demo
----

.. image:: https://user-images.githubusercontent.com/5244214/102778186-6729a200-4392-11eb-981a-b2f3db50c2b9.gif
  :alt: Gaze Example Demo
  :target: https://www.youtube.com/watch?v=yNFgp1xrE80

Install
-------

.. code-block:: bash

    pip install depthai-gui

Usage
-----

To start the GUI, run

.. code-block:: bash

    depthai-gui

To run a specific example (:code:`example.pygraph`) run

.. code-block:: bash

    depthai-gui -f /path/to/example.pygraph

Troubleshooting
---------------

AttributeError: module 'Qt' has no attribute 'QtGui'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We experienced this issue with Qt library on Ubuntu 18.04, and the cause
of this error was in missing libraries.

To make it work, please make sure you have the following libraries
installed:

.. code-block:: bash

    sudo apt-get install libgl1-mesa-glx libpulse-dev libxcb-xinerama0 libfontconfig libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xkb1 libxkbcommon-x11-0

`Here <https://gist.github.com/VanDavv/62d1940f83fe2059f4734a5a7b40caf7>`__
is a gist showing a working Ubuntu 18.04 example installation based on Docker.
