#/bin/bash

xhost +

docker run -dit \
    --name IntelPi \
    --privileged \
    --restart always \
    --network=host \
    -e DISPLAY=${DISPLAY} \
    -e XAUTHORITY=/home/ubuntu/.Xauthority \
    -v ~/.Xauthority:/home/ubuntu/.Xauthority:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unit \
    -v ${HOME}/ros2_ws:/ros2_ws \
    -v ${HOME}/docker_tutorial/shared:/shared \
    -v /dev:/dev \
    ros:humble-export \
    tail -f /dev/null
