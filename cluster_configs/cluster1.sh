#!/bin/bash
export MAIN_CLUSTER_CTX=kind-kind-1
export MAIN_CLUSTER_NAME=kind-1
export REMOTE_CLUSTER_NAME=kind-2
export MAIN_CLUSTER_NETWORK=network1
export REMOTE_CLUSTER_NETWORK=network1

kubectl config use-context $MAIN_CLUSTER_CTX

kubectl create namespace istio-system
kubectl create secret generic cacerts -n istio-system \
    --from-file=samples/certs/ca-cert.pem \
    --from-file=samples/certs/ca-key.pem \
    --from-file=samples/certs/root-cert.pem \
    --from-file=samples/certs/cert-chain.pem

istioctl --context=${MAIN_CLUSTER_CTX} install --set profile=demo

istioctl --context=${MAIN_CLUSTER_CTX} install -f istio-cluster1.yaml

# Wait

kubectl get pod -n istio-system --context=${MAIN_CLUSTER_CTX}
export ISTIOD_REMOTE_EP=$(kubectl get svc -n istio-system --context=${MAIN_CLUSTER_CTX} istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "ISTIOD_REMOTE_EP is ${ISTIOD_REMOTE_EP}"

kubectl apply --context=${MAIN_CLUSTER_CTX} -f ns.yaml

kubectl -n istio-thrift --context=${MAIN_CLUSTER_CTX} apply -f cluster1.yaml

# Wait

kubectl -n istio-thrift --context=${MAIN_CLUSTER_CTX} apply -f gateway.yaml

export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].nodePort}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].nodePort}')
export TCP_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="tcp")].nodePort}')
export INGRESS_HOST=$(kubectl get po -l istio=ingressgateway -n istio-system -o jsonpath='{.items[0].status.hostIP}')
export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT