# Exercise 3: Performance and Monitoring
## Objective: Monitor and optimize container performance


### creating a docker network for containers to run in
```
sudo docker network create prom-network
```

### running prometheus contianer

```
sudo docker container run -d \
--name prom-monitor \
-port 9090:9090 \
-v /promtheus.yml:/etc/prometheus/prometheus.yml
--network prom-network
ubuntu/prometheus
```


### running grafana container 

```
sudo docker container run -d \
--name grafana-monitor \
-p 3000:3000 \
--network prom-network \ 
grafana/grafana:latest
```




### Bonus: running node exporter container to be monitored by prometheus

```
sudo docker container run -d \
--name node
--network prom-network
bitnami/node-exporter
```
