### Environment Setup
* You need to  have virtualbox installed 
* Install Docker Desktop for Mac or Docker Desktop for Windows

###  Create the docker machine
Create one docker machine called dockerlabor
$ docker-machine create --driver virtualbox dockerlabor
$ docker node ls

```
--virtualbox-cpu-count "1"      number of CPUs for the machine (-1 to use the number of CPUs available) [$VIRTUALBOX_CPU_COUNT]
--virtualbox-memory "1024"      Size of memory for host in MB [$VIRTUALBOX_MEMORY_SIZE]
```

$ docker-machine create --driver  virtualbox  --virtualbox-cpu-count "4" --virtualbox-memory "4096" workerA

$ docker swarm join-token worker

$ docker-machine ssh  workerA


### Setup local volume for applications
$ docker-machine ssh dockerlabor
$ mkdir -p volumes/data volumes/log volumes/media volumes/statics
$ sudo chown -R 999:999 volumes/data volumes/log

### deploy docker stack, utilize the environment variable inside .env file
$ env $(cat .env | grep ^[A-Z] | xargs) docker stack deploy --compose-file docker-compose-stack.yaml seckill

### view the service status
docker stack ls
docker service ls


