# Create network test environment

### Requirements
```
echo "source <(kubectl completion bash)" >> ~/.bashrc
source ~/.bashrc

apt-get update 
apt-get install -y iproute2
apt-get install -y socat
```

## UDP Multicast
To check UDP multicast within your Kubernetes pods, you can follow these steps:

Verify Multicast Support: Ensure that your CNI plugin supports multicast. Not all CNI plugins provide native support for multicast, so you need to check if yours does. For example, Calico and Weave Net both support multicast.

Deploy Test Pods: Deploy three pods within your Kubernetes cluster. These pods will be used to test UDP multicast communication.

Install Tools for Testing: You might need to install tools like socat or netcat inside the pods to create and listen to UDP multicast traffic.

Run Multicast Test: Within each pod, you can use tools like socat or netcat to send and receive UDP multicast traffic. Here's an example using socat:

```
# Install socat if not already installed
apt-get update && apt-get install -y socat

# Start a listener on each pod
socat UDP4-LISTEN:12345,ip-add-membership=239.0.0.1:eth0,reuseaddr,fork -
```
Replace eth0 with your network interface if needed and 12345 with the desired port.

Send Multicast Traffic: From one of the pods, send UDP multicast traffic:

```
# Install socat if not already installed
apt-get update && apt-get install -y socat

# Send multicast traffic
echo "Hello, multicast!" | socat - UDP4-DATAGRAM:239.0.0.1:12345,ttl=1
```
Replace 239.0.0.1 with the multicast group address and 12345 with the port you're using.

Verify Reception: Check if the other pods receive the multicast traffic. You should see the message "Hello, multicast!" on the consoles of the other pods.

Network Policies (if applicable): If you have Network Policies in place, ensure that they allow UDP multicast traffic between these pods.

By following these steps, you can test UDP multicast communication within your Kubernetes pods. Make sure to adjust the commands according to your specific setup and requirements.

## Wavenet Installation

### Wavenet Installation

## Experiments

- before waveneet I can not see the mulicast address. 

On pod1 => 1.10
nc -vz 10.244.2.8 1234

On pod2
nc -vz 10.244.1.10 1234


On pod1 => 1.10
echo "Hello, pod2" | nc -u -w1 10.244.2.8 12345

On pod2 => 2.8
nc -u -l -p 12345