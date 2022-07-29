---
title: "3D Xmas Tree Programming"
date: 2022-07-29T23:09:43+01:00
tags:
    - Programming
category:
    - blog
keywords:
    - Programming
    - 3d xmas
    - opencv
draft: true
---

The 3d xmas christmas challenge is a programming task first created by the yt channel [Stand up maths](https://www.youtube.com/user/standupmaths).
It was first showcased in 2020 [in this video](https://www.youtube.com/watch?v=TvlpIojusBE).
This is my attempt at recreating the video.

## Brief

Using python+opencv, I plan to calculate the 3d position of the camera relative to a fixed point.
Then cast rays towards each individual led and calculate the led position relative to the camera and the fixed point.
Once finished, i can save this data in an array and access run some interesting 3d led effects.

## The Plan

1.
    Camera calibration.
    The camera has a distorted lense and wont track accurately. "garbage in, garbage out"

    I will be following [this guide here](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)

2.
    Calculate 3D position of camera.
    The camera needs to use an ArUco Board to find its position in 3d space.
    It can be then used to calculate the led's position relative.

    I'll be using another openCV [guild](https://docs.opencv.org/4.x/db/da9/tutorial_aruco_board_detection.html) to do this.

3.
    Casting rays at the led.
    Ill use simple image processing && filtering to find the brightest pixel on the screen.
    Then cast a ray (relative to "origin")

4.
    Calculate the closest point of intercept between rays.
    Because of inaccuracies in image processing, no two rays will be perfectly accurate.
    Its gonna take a lot of really complicated new maths that i don't understand to work this out.

    [stackoverflow is my new friend](https://math.stackexchange.com/questions/2598811/calculate-the-point-closest-to-multiple-rays)

## Coding

All my code will be linked on [github](https://github.com/Blotz/3d-xmas-tree)

### Camera calibration
