# DECICE-UC3

## Docker
`docker build -t uc3 .`

`docker run -it --name uc3-container uc3`


docker build -t my-custom-image:latest /path/to/Dockerfile

docker tag uc3:latest localhost:5000/uc3:latest

docker run -d -p 5000:5000 --restart=always --name registry registry:2


docker push localhost:5000/uc3:latest


## Kubernetes 
`
docker tag uc3:latest localhost:5000/uc3:latest
`

`
kubectl run my-pod --image=localhost:5000/uc3:latest --restart=Never

`

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
source ~/.bashrc```