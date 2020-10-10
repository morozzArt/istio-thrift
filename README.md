# istio-thrift

1. Create kubernetes cluster in docker

```
kind create cluster
```

2. Run and setup istio

```
istioctl install --set profile=demo
```

3. Build docker images for services

```
docker build -t client/client:some_tag Clients/client1
docker build -t country/country:some_tag Services/Country
```

4. Load an images into cluster

```
kind load docker-image client/client:some_tag
kind load docker-image country/country:some_tag
```

5. Apply the cluster settings

```
kubectl apply -f ns.yaml
kubectl -n istio-thrift apply -f deploy.yaml
```

6. Define the ingress gateway:

```
kubectl -n istio-thrift apply -f gateway.yaml
```

7. Follow [these instructions](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/#determining-the-ingress-ip-and-ports) to set the INGRESS_HOST and INGRESS_PORT variables for accessing the gateway. Return here, when they are set.
