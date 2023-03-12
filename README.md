# nvidia-docker_VirtualMachine3

This repository is what I re-created as Streaming server of Web camera with FaceRecogizer I created before as below: 
- https://github.com/developer-onizuka/nvidia-docker_VirtualMachine2

What you should do is only "vagrant up --provider=libvirt" in step#0 below, But you can learn all of the steps:

# 0. Vagrant Up at Host Machine
```
$ git clone https://github.com/developer-onizuka/nvidia-docker_VirtualMachine3
$ cd nvidia-docker_VirtualMachine3
$ vagrant up --provider=libvirt
```

If you wanna change images directry from /var/lib/libvirt/images to some another directry, you might use followings:
```
$ mkdir -p /mnt/data
$ virsh pool-create-as --name data --type dir --target /mnt/data
$ virsh pool-list
 Name      State    Autostart
-------------------------------
 data      active   no
 default   active   no
```

You also change the Vagrantfile as follow, if you changed the directry above.
```
  config.vm.provider "libvirt" do |kvm|
    kvm.storage_pool_name = "data"
```

You can destroy it if it's not necessary any more.
```
$ virsh pool-destroy <pool_name>
```

# 1. Create docker container image using the Dockerfile attached at Virtual Machine
```
$ git clone https://github.com/developer-onizuka/nvidia-docker_VirtualMachine3
$ cd nvidia-docker_VirtualMachine3
$ ls -trl
total 48
-rw-rw-r-- 1 onizuka onizuka  4286 Oct 24 19:19 Vagrantfile
-rw-rw-r-- 1 onizuka onizuka 14190 Oct 24 19:19 train.pkl
-rwxrwxr-x 1 onizuka onizuka  1741 Oct 24 19:19 test.py
drwxrwxr-x 2 onizuka onizuka  4096 Oct 24 19:19 templates
-rw-rw-r-- 1 onizuka onizuka  2467 Oct 24 19:19 README.md
-rw-rw-r-- 1 onizuka onizuka   921 Oct 24 19:19 Dockerfile
-rwxrwxr-x 1 onizuka onizuka  2240 Oct 24 19:19 camera.py
-rwxrwxr-x 1 onizuka onizuka  1087 Oct 24 19:19 app.py
-rw-r--r-- 1 vagrant vagrant  4286 Oct 24 07:13 Vagrantfile

$ ls -trl templates/
total 8
-rw-rw-r-- 1 onizuka onizuka 271 Oct 24 19:19 stream.html
-rw-rw-r-- 1 onizuka onizuka 198 Oct 24 19:19 index.html

$ sudo docker build -t face_recognizer:1.0.1 .
```

# 2. Run containerized nvidia driver at Virtual Machine
```
$ sudo docker run --name nvidia-driver -itd --rm --privileged --pid=host -v /run/nvidia:/run/nvidia:shared -v /var/log:/var/log  nvcr.io/nvidia/driver:470.57.02-ubuntu20.04
$ sudo docker logs -f nvidia-driver
```

New Driver (released on 02/16/2023 10:42 AM)
```
$ sudo docker run --name nvidia-driver -itd --rm --privileged --pid=host -v /run/nvidia:/run/nvidia:shared -v /var/log:/var/log  nvcr.io/nvidia/driver:525.85.12-ubuntu20.04
```

# 3. Run containerized web Face_recognized streaming server at Virtual Machine
Access the URL informed by the command below:
```
$ sudo docker run -it --net host -v /tmp/test:/mnt -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority --device /dev/video0:/dev/video0:mwr -e DISPLAY=$DISPLAY --gpus all --rm --name="camera" face_recognizer:1.0.1
```

```
$ sudo docker run -it --net host -v /tmp/test:/mnt -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/root/.Xauthority --device /dev/video0:/dev/video0:mwr -e DISPLAY=$DISPLAY --gpus all --rm --name="camera" face_recognizer:1.0.1
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.121.243:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 138-385-403
192.168.121.1 - - [12/Mar/2023 00:34:58] "GET / HTTP/1.1" 200 -
192.168.121.1 - - [12/Mar/2023 00:34:58] "GET /favicon.ico HTTP/1.1" 500 -
...
```

# X. Optional steps
If you found "[ WARN:1] global ../modules/videoio/src/cap_v4l.cpp (887) open VIDEOIO(V4L2:/dev/video0): can't open camera by index", You might use followings steps.

https://stackoverflow.com/questions/59371075/opencv-error-cant-open-camera-through-video-capture
```
$ sudo apt-get update && DEBIAN_FRONTEND='noninteractive' sudo apt-get install -y libx11-dev python3-distutils python3-setuptools python3-pip python3-opencv git cmake libopenblas-dev liblapack-dev libjpeg-dev
$ id -a
$ ls -l /dev/video0
$ sudo usermod -a -G video vagrant
$ id -a
$ exit 
and Login again
```
