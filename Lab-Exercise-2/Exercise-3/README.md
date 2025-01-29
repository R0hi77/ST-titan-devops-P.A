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
-v /alertrules.yml:/etc/prometheus/alertrule.yml
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

### running alert manager

```
sudo docker container run -d \
--name alert-monitor \
-p 9093:9093 \
-- network prom-network
prom/alertmanager:latest
```


### Bonus: running node exporter container to be monitored by prometheus

```
sudo docker container run -d \
--name node
--network prom-network
bitnami/node-exporter
```
