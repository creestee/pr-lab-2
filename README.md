# Network Programming, TUM

First web server is `Factory-Module`, which produces some data and send it to the second web server, which is called `Aggregator-Module`, which receives and aggregates data from first server and populates a Thread-Safe queue, also sends its data to a third server called `Delivery-Module`, which receives and consumes data from second server and populates another queue.

## Setup and running

First clone the repository 

```
https://github.com/creestee/pr
```

After that, make sure you have Docker and Docker Compose installed and also check that docker service is running inside your OS

https://docs.docker.com/engine/install/

Finally, run command, that starts up both containers

```
docker compose up --build
```