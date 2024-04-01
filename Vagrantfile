# -*- mode: ruby -*-
# vi: set ft=ruby :

vm_name_cp = "vmcp"
vm_name_w1 = "vmw1"
vm_name_w2 = "vmw2"

vm_ip_cp = "192.168.56.10"
vm_ip_w1 = "192.168.56.11"
vm_ip_w2 = "192.168.56.12"



Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"
  config.vm.synced_folder "/home/mohsen/scratch", "/mohsen"
  config.vm.provision "shell", path: "provision_all.sh"
  config.vm.provision "shell", path: "CRI_DockerEng_containerd.sh"
  config.vm.provision "shell", path: "kubeadm_kubelet_kubectl.sh"

  config.vm.provision "shell", inline: "echo '#{vm_ip_cp} #{vm_name_cp}' | sudo tee -a /etc/hosts"
  config.vm.provision "shell", inline: "echo '#{vm_ip_w1} #{vm_name_w1}' | sudo tee -a /etc/hosts"
  config.vm.provision "shell", inline: "echo '#{vm_ip_w2} #{vm_name_w2}' | sudo tee -a /etc/hosts"


  # Control Plane Configuration
  config.vm.define vm_name_cp do |cp|
    cp.vm.network "private_network", ip: vm_ip_cp
    cp.vm.hostname = vm_name_cp  # This sets the internal hostname of the VM
    cp.vm.provider "virtualbox" do |vb|
      vb.name = vm_name_cp # This sets the name displayed in VirtualBox
      vb.memory = "10240" # This sets the amount of memory for the VM
      vb.cpus = 8 # This sets the number of CPUs for the VM
    end
    cp.vm.provision "shell", path: "create_cluster.sh"
  end

  # Worker Node 1 Configuration
  config.vm.define vm_name_w1 do |w1|
    w1.vm.network "private_network", ip: vm_ip_w1
    w1.vm.hostname = vm_name_w1 # This sets the internal hostname of the VM
    w1.vm.provider "virtualbox" do |vb|
      vb.name = vm_name_w1 # This sets the name displayed in VirtualBox
      vb.memory = "6096" # This sets the amount of memory for the VM
      vb.cpus = 2 # This sets the number of CPUs for the VM
    end
    w1.vm.provision "shell", inline: "bash /vagrant/join-command.sh"
  end


  # Worker Node 2 Configuration
  config.vm.define vm_name_w2 do |w2|
    w2.vm.network "private_network", ip: vm_ip_w2
    w2.vm.hostname = vm_name_w2 # This sets the internal hostname of the VM
    w2.vm.provider "virtualbox" do |vb|
      vb.name = vm_name_w2 # This sets the name displayed in VirtualBox
      vb.memory = "6096" # This sets the amount of memory for the VM
      vb.cpus = 2 # This sets the number of CPUs for the VM
    end
    w2.vm.provision "shell", inline: "bash /vagrant/join-command.sh"
  end


end





# source /opt/ros/foxy/setup.bash
# ros2 run demo_nodes_cpp talker

# source /opt/ros/foxy/setup.bash
# ros2 run demo_nodes_cpp listener

# $ kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml

# kubectl delete -f https://raw.githubusercontent.com/cilium/cilium/v1.9/install/kubernetes/quick-install.yaml
# kubectl apply  -f https://raw.githubusercontent.com/cilium/cilium/v1.15/install/kubernetes/quick-install.yaml


# kubectl delete -f  https://raw.githubusercontent.com/projectcalico/calico/v3.26.0/manifests/calico.yaml
# kubectl apply  -f  https://raw.githubusercontent.com/projectcalico/calico/v3.26.0/manifests/calico.yaml

# kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
# kubectl delete -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
# ----------------------------------------------


# virtual_machine_1_name = "vmcp"
# virtual_machine_2_name = "vmw1"
# virtual_machine_3_name = "vmw2"

# Vagrant.configure("2") do |config|
#   config.vm.synced_folder "/home/mohsen/scratch", "/mohsen"
#   config.vm.box = "ubuntu/jammy64"
#   config.vm.provision "shell", path: "provision.sh"
  
#   # # SSH Key Configuration
#   # config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "/home/vagrant/temp_id_rsa.pub"
#   # config.vm.provision "shell", inline: <<-SHELL
#   #   cat /home/vagrant/temp_id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
#   #   rm /home/vagrant/temp_id_rsa.pub
#   # SHELL

#   # VM1 Configuration
#   config.vm.define virtual_machine_1_name do |vm1|
#     vm1.vm.network "private_network", ip: "192.168.56.10"
#     vm1.vm.hostname = virtual_machine_1_name  # This sets the internal hostname of the VM
#     vm1.vm.provider "virtualbox" do |vb|
#       vb.name = virtual_machine_1_name # This sets the name displayed in VirtualBox
#       vb.memory = "10240" # This sets the amount of memory for the VM
#       vb.cpus = 8 # This sets the number of CPUs for the VM
#     end
#     vm1.vm.provision "shell", inline: <<-SHELL
#       sudo apt-get update
#       sudo kubeadm init --apiserver-advertise-address=192.168.56.10 --pod-network-cidr=10.244.0.0/16
   
#       mkdir -p /home/vagrant/.kube
#       sudo cp -i /etc/kubernetes/admin.conf /home/vagrant/.kube/config
#       sudo chown vagrant:vagrant /home/vagrant/.kube/config
#       sudo chown vagrant:vagrant /home/vagrant/.kube
    
#       # mkdir -p $HOME/.kube
#       # sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
#       # sudo chown $(id -u):$(id -g) $HOME/.kube/config
      
#       # # Apply Flannel CNI network overlay
#       # kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

#       # Save the join command to a shared location
#       kubeadm token create --print-join-command > /vagrant/join-command.sh
#       # Auto-completion for kubectl
#       sudo apt-get update
#       sudo apt-get -y install bash-completion
#       kubectl completion bash > ~/.kube/kubectl_bash_completion
#       echo "source ~/.kube/kubectl_bash_completion" >> ~/.bashrc
#       source ~/.bashrc
#     SHELL
#   end
  
#   # VM2 Configuration
#   config.vm.define virtual_machine_2_name do |vm2|
#     vm2.vm.network "private_network", ip: "192.168.56.11"
#     vm2.vm.hostname = virtual_machine_2_name # This sets the internal hostname of the VM
#     vm2.vm.provider "virtualbox" do |vb|
#       vb.name = virtual_machine_2_name # This sets the name displayed in VirtualBox
#       vb.memory = "4096" # This sets the amount of memory for the VM
#       vb.cpus = 2 # This sets the number of CPUs for the VM
#     end
#     vm2.vm.provision "shell", inline: "bash /vagrant/join-command.sh"
#   end

#   # VM3 Configuration
#   config.vm.define virtual_machine_3_name do |vm3|
#     vm3.vm.network "private_network", ip: "192.168.56.12"
#     vm3.vm.hostname = virtual_machine_3_name # This sets the internal hostname of the VM
#     vm3.vm.provider "virtualbox" do |vb|
#       vb.name = virtual_machine_3_name # This sets the name displayed in VirtualBox
#       vb.memory = "4096" # This sets the amount of memory for the VM
#       vb.cpus = 2 # This sets the number of CPUs for the VM
#     end
#     vm3.vm.provision "shell", inline: "bash /vagrant/join-command.sh"
#   end

#   # # Define a local trigger after `vagrant up` completes to apply additional provisioning on vm1
#   # config.trigger.after :up do |trigger|
#   #   trigger.info = "Applying Flannel CNI network overlay on #{virtual_machine_1_name}..."
#   #   trigger.only_on = virtual_machine_3_name # Ensures this trigger runs only after vm3 is up
#   #   trigger.run = {inline: "vagrant ssh #{virtual_machine_1_name} -c 'kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml'"}
#   # end
# end

# # =====================================
# # Vagrant.configure("2") do |config|
# #     (1..2).each do |i|
# #       config.vm.define "node#{i}" do |node|
# #         node.vm.box = "ubuntu/jammy64"
# #         node.vm.network "private_network", type: "dhcp"
# #         node.vm.provision "shell", inline: <<-SHELL
# #           apt-get update
# #         SHELL
# #       end
# #     end
# #   end
  