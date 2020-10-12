#!/bin/bash
export MAIN_CLUSTER_CTX=kind-kind-1
export REMOTE_CLUSTER_CTX=kind-kind-2

export MAIN_CLUSTER_NAME=kind-1
export REMOTE_CLUSTER_NAME=kind-2

export MAIN_CLUSTER_NETWORK=network1
export REMOTE_CLUSTER_NETWORK=network1

kubectl config use-context ${REMOTE_CLUSTER_CTX}

kubectl create namespace istio-system
kubectl create secret generic cacerts -n istio-system \
    --from-file=samples/certs/ca-cert.pem \
    --from-file=samples/certs/ca-key.pem \
    --from-file=samples/certs/root-cert.pem \
    --from-file=samples/certs/cert-chain.pem

istioctl --context=${REMOTE_CLUSTER_CTX} install --set profile=demo

istioctl --context=${REMOTE_CLUSTER_CTX} install -f istio-cluster2.yaml

# Wait for cluster to be ready

kubectl get pod -n istio-system --context=${REMOTE_CLUSTER_CTX}


istioctl x create-remote-secret --name ${REMOTE_CLUSTER_NAME} --context=${REMOTE_CLUSTER_CTX} | \
    kubectl apply -f - --context=${MAIN_CLUSTER_CTX}

kubectl apply --context=${REMOTE_CLUSTER_CTX} -f ns.yaml

kubectl -n istio-thrift --context=${REMOTE_CLUSTER_CTX} apply -f cluster2.yaml