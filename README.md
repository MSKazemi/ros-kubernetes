# DECICE-UC3

Steps:
I will check the codes of Sebatiano in Docker using the  docker.io/px4io/px4-dev-ros2-foxy:latest image.
The next step is to check the codes of Sebatiano in Kubernetes using the same image.
The next step is adding new node and check the communication between the nodes.




## Docker



```
docker build -t uc3 .

docker build -t uc3-unibo /home/mohsen/scratch/DECICE-UC3/ -f  /home/mohsen/scratch/DECICE-UC3/Dockerfile-px4
docker run -it --rm --name test uc3-unibo

docker run -it --name uc3-container uc3
docker run -it --rm --name uc3-container px4io/px4-dev-ros2-foxy

```
### Local Registery
It is was not successful.
```
docker build -t my-custom-image:latest /path/to/Dockerfile
docker tag uc3:latest localhost:5000/uc3:latest
docker run -d -p 5000:5000 --restart=always --name registry registry:2
docker push localhost:5000/uc3:latest



docker tag uc3:latest localhost:5000/uc3:latest

```

### ROS2 & PX4 Docker
```
Three Scenarios :
    1- Create your own Dockerfile and create image
    2- find a Dockerfile from Internet and update/complete it
    3- Pull image from docker registery 
        A)  https://hub.docker.com/u/px4io/
            docker pull px4io/px4-dev-ros2-foxy
        B)  Two node in single docker
            docker pull osrf/ros:foxy-desktop
            https://docs.ros.org/en/foxy/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html
 

```


## Kubernetes 

```
kubectl run my-pod --image=localhost:5000/uc3:latest --restart=Never
```

### Kind
To connet from my laptop which is not part of the kubernetes cluster I need to install kubectl and then config the context with config file.
- For runing the kubectl I could not do it from my laptop I should connect to the docker container `docker exec -it kind-control-plane /bin/bash`. The from that node which is docker container I can run the K8s commands.
Copy config file from then kind nodes with docker exec... and then with this config file from my laptop connet directly to the cluster.
But this has a problem since the server should config to right one and also the defualt port should update. We can find the correct porn and server from runing docker ps and checking that PORTS.
The all secret and user names should keep same/
 
## Open Questions:
- Q1: How I can use my local images in defintions of the pod. I mean I create an image in my local computer but I did not push to the docker regitery.




---
## Enable kubectl autocompletion
```

sudo apt update
sudo apt install bash-completion

kubectl completion bash > ~/.kube/kubectl_bash_completion
echo "source ~/.kube/kubectl_bash_completion" >> ~/.bashrc
source ~/.bashrc
```


# ROS2 - Today 2024-02-28
I am try to learn ROS2 consepets and also how to use it in Docker and Kubernetes.
I will start with Docker and then I will move to Kubernetes.
I will use the following links:
https://www.youtube.com/watch?v=3GbrKQ7G2P0&list=PLLSegLrePWgJudpPUof4-nVFHGkB62Izy&index=3

So I should create workspace and then build it (create node) and source it in bashrc.
 - create with `colcon build`
 - `ros2 pkg create my_robot_controller --build-type ament_python --dependencies rclpy`  
 - package can have many nodes.

https://docs.ros.org/en/foxy/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html 

```
docker pull osrf/ros:foxy-desktop
docker run -it --name ros2 osrf/ros:foxy-desktop
docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name ros3 osrf/ros:foxy-desktop
```



```
apt update


echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc

apt install -y screen vim 

echo "shell bash" >> ~/.screenrc


ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_cpp listener
rqt_graph
 
```

flannel is CNI plugin for Kubernetes. But the problem with ROS is it is not support multicast which use by ROS for service discovery. 
ROS2 or DDS use multicast for service discovery.
Wavenet is a CNI plugin for Kubernetes that supports multicast and UDP.

