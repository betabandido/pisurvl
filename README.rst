Surveillance system based on Raspberry Pi.

Pisurvl is a surveillance solution with motion detection and alert notifications. This repository contains the server
part of the solution. It is implemented in Python and it uses `OpenCV`_ to access the camera of the Raspberry Pi. Despite
being implemented on top of a Raspberry Pi, the solution should work on any system having a camera that is supported
by OpenCV.

Installation
============

Installing OpenCV
----------------------

Currently there is no easy way to install OpenCV 3 on Linux. The following commands install all the necessary
dependencies to build OpenCV 3:

.. code:: bash

   sudo apt install build-essential cmake git pkg-config
   sudo apt install libgtk2.0-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
   sudo apt install libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
   sudo apt install libatlas-base-dev gfortran liblapacke-dev
   sudo apt install python3 python3-dev python3-setuptools
   sudo easy_install3 pip

The following command installs the latest version of Numpy. The installation may take a while to complete.

.. code:: bash

   sudo pip3 install numpy

The following commands download and compile OpenCV 3:

.. code:: bash

   mkdir build-opencv && cd build-opencv
   git clone https://github.com/opencv/opencv.git
   git clone https://github.com/opencv/opencv_contrib.git
   cd opencv_contrib && git checkout 3.2.0 && cd ..
   cd opencv && git checkout 3.2.0
   mkdir build && cd build
   cmake -D CMAKE_BUILD_TYPE=Release \
     -D CMAKE_INSTALL_PREFIX=/usr/local \
     -D OPENCV_EXTRA_MODULES_PATH=`pwd`/../../opencv_contrib/modules \
     ..
   make -j4

Then install OpenCV:

.. code:: bash

   sudo make install



Installing PiSurvl
------------------

.. code:: bash

   sudo pip3 install pisurvl
   git clone https://github.com/betabandido/pisurvl.git
   sudo cp pisurvl/init/pisurvl.service /etc/systemd/system
   sudo systemctl enable pisurvl.service

.. _OpenCV: http://opencv.org
