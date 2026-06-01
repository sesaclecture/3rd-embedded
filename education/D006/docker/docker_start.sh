#/bin/bash

xhost +

docker run -it --rm --name humble-gui \
    --network=host \
    --name=MentoPi \
    -e DISPLAY=${DISPLAY} \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -e ROS_DOMAIN_ID=36 \
    -e RMW_IMPLEMENTATION=rmw_cyclonedds_cpp \
    -e XAUTHORITY=/root/.Xauthority \
    -v ~/.Xauthority:/root/.Xauthority:ro \
    -v /tmp/.X11-unix:/tmp/.X11-unit \
    -v ${HOME}/ros2_ws:/ros2_ws \
    -v ${HOME}/docker_tutorial/shared:/shared \
    arm64v8/ros:humble \
    /bin/bash
