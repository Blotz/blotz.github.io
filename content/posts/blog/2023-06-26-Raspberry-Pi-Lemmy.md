---
title: "Raspberry Pi Lemmy"
date: 2023-06-26T12:46:31+01:00
tags:
    - Self-hosting
    - Lemmy
    - Raspberry Pi
category:
    - blog
keywords:
    - lemmy
    - raspberry pi
    - self host
    - raspberry pi 3b
comments: true
draft: true
---

This is going to be an informal write up of how I setup a Lemmy Instance on my Raspberry Pi.
I will be writing this as I set it up, which means any mistakes I make will be included and how I resolved them.

This is a very informal and unofficial guide.

## Setting up Raspberry Pi

I am starting from a fresh raspberry pi 3b with nothing setup. No OS on an sd card or anything.

### Installing OS

Using rpi-imager, I am flashing the 64bit raspberry pi os lite over. 
In addition, I am using the rpi-imager config settings to flash over ssh keys and enable ssh.

And its all working, running nmap shows.

After ssh-ing in to confirm its all working, I'll update the pi to ensure everything is up to date.

## Lemmy Install 

Now that I have the basics, I need to set up some of the server side software.
This includes:

- docker
- docker-compose

In addition, I want to use docker-rootless.

This is as simple as going to dockers's [website](https://docs.docker.com/engine/install/raspbian/#install-using-the-convenience-script) and using their convenience script.

### Installing rootless-docker

Follow the docker install docs [here](https://docs.docker.com/engine/install/raspbian/)

```bash
apt-get install -y uidmap
```

Adding new user. (I'm unsure whether this can be `docker` because the docker group adds extra permissions which might be unintended)

```bash
adduser --disabled-login docker-user
loginctl enable-linger docker-user
echo 'export XDG_RUNTIME_DIR=/run/user/$(id -u)' >> /home/docker-user/.bashrc
su - docker-user
```

Now as the docker user.

Make sure systemd is working by running: 

```bash
$ export XDG_RUNTIME_DIR=/run/user/$(id -u)
$ systemctl --user
```

You could also add the export line to your bashrc to avoid having to re-enter it

Install!

```bash
$ dockerd-rootless-setuptool.sh install
```

follow the instructions in the command output!

### Setup Lemmy Container

#### Configure Docker-Rootless

setup [privileged ports](https://docs.docker.com/engine/security/rootless/#exposing-privileged-ports).

as root user run
```bash
setcap cap_net_bind_service=ep $(which rootlesskit)
```

then restart the docker service as your user
```bash
$ systemctl --user restart docker
```

#### Setup Lemmy Configs

Download and extract latest release. eg.

```bash
$ mkdir lemmy
$ cd lemmy
$ wget https://raw.githubusercontent.com/LemmyNet/lemmy/release/v0.17/docker/prod/docker-compose.yml
```

Modify your docker compose by updating the image to point to an arm image.
Please refer to dockerhub to see if a newer arm version has been released.

```patch
--- docker-compose.yml.bak	2023-06-26 18:53:56.514418534 +0100
+++ docker-compose.yml	2023-06-26 18:55:19.921852021 +0100
@@ -29,7 +29,7 @@
       - lemmy-ui

   lemmy:
-    image: dessalines/lemmy:0.17.4
+    image: dessalines/lemmy:0.17.3-linux-arm64
     hostname: lemmy
     networks:
       - lemmyinternal
@@ -43,7 +43,7 @@
       - pictrs

   lemmy-ui:
-    image: dessalines/lemmy-ui:0.17.4
+    image: dessalines/lemmy-ui:0.17.3-linux-arm64
     networks:
       - lemmyinternal
     environment:
```

start lemmy instance using.

```bash
$ docker compose up
```

ugh this doesnt work kmn
