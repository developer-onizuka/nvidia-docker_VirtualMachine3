# nvidia-docker_VirtualMachine3

This repository is for creating Streaming server of Web camera with FaceRecogizer below: 
- https://github.com/developer-onizuka/nvidia-docker_VirtualMachine2

What you should do is "vagrant up --provider=libvirt", But you can learn all of the steps below:

# 0. Vagrant Up at Host Machine
```
$ git clone https://github.com/developer-onizuka/nvidia-docker_VirtualMachine3
$ cd nvidia-docker_VirtualMachine3
$ vagrant up --provider=libvirt
```

# 1. Create docker container image using the Dockerfile attached at Virtual Machine
```
$ git clone https://github.com/developer-onizuka/nvidia-docker_VirtualMachine3
$ cd nvidia-docker_VirtualMachine3
$ ls -trl
total 60
-rw-r--r-- 1 vagrant vagrant 14190 Oct 16 10:51 train.pkl
-rwxr-xr-x 1 vagrant vagrant  1741 Oct 16 10:51 test.py
-rw-r--r-- 1 vagrant vagrant 10261 Oct 16 10:51 README.md
drwxrwxr-x 2 vagrant vagrant  4096 Oct 24 03:05 templates
-rwxr-xr-x 1 vagrant vagrant  2242 Oct 24 06:54 camera.py
-rw-r--r-- 1 vagrant vagrant   921 Oct 24 07:01 Dockerfile
-rwxrwxr-x 1 vagrant vagrant   766 Oct 24 07:02 app.py
-rw-r--r-- 1 vagrant vagrant  4286 Oct 24 07:13 Vagrantfile

$ sudo docker build -t face_recognizer:1.0.1 .
```

# 2. Run containerized nvidia driver at Virtual Machine
```
$ sudo docker run --name nvidia-driver -itd --rm --privileged --pid=host -v /run/nvidia:/run/nvidia:shared -v /var/log:/var/log  nvcr.io/nvidia/driver:470.57.02-ubuntu20.04

$ sudo docker logs -f nvidia-driver
```

# 3. Run containerized web Face_recognized streaming server at Virtual Machine
```
$ sudo docker run -it --net host -v /tmp/test:/mnt -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority --device /dev/video0:/dev/video0:mwr -e DISPLAY=$DISPLAY --gpus all --rm --name="camera" face_recognizer:1.0.1
```

# 4. Optional steps
If you found "[ WARN:1] global ../modules/videoio/src/cap_v4l.cpp (887) open VIDEOIO(V4L2:/dev/video0): can't open camera by index", You might use followings steps.

https://stackoverflow.com/questions/59371075/opencv-error-cant-open-camera-through-video-capture
```
$ sudo apt-get update && DEBIAN_FRONTEND='noninteractive' sudo apt-get install -y libx11-dev python3-distutils python3-setuptools python3-pip python3-opencv git cmake libopenblas-dev liblapack-dev libjpeg-dev
$ id -a
$ ls -l /dev/video0
$ sudo usermod -a -G video vagrant
$ id -a
```
