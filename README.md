# triton

```export DOCKER_BUILDKIT=0```

```docker build -t triton . ```

```docker run --name triton -d --env SERVER_TOKEN= --env SERVER_IP= --env SERVER_PORT= --env SERVER_PREFIX= triton:latest```