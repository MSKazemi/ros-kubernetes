kind delete cluster -n mska
kind create cluster --name mska --config kind-config.yaml


kubectl apply -f https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s-1.11.yaml

