# Use the official Ubuntu base image
FROM ubuntu:latest

# Update the package lists
RUN apt-get update -y && apt-get upgrade -y

# Install any necessary packages
# For example, to install curl:
# RUN apt-get install -y curl

RUN apt install -y curl
RUN apt install -y locales
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8
RUN apt install -y software-properties-common
RUN add-apt-repository universe
RUN apt update 
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN apt update && sudo apt upgrade -y
RUN apt install ros-humble-desktop
RUN o apt install ros-dev-tools
RUN source /opt/ros/humble/setup.bash && echo "source /opt/ros/humble/setup.bash" >> .bashrc


# Any additional setup or configuration can go here

# Default command to execute when the container starts
CMD ["bash"]
