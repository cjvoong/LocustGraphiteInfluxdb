#!/usr/bin/env bash -x

## Create jmeter database automatically in Influxdb

echo "Creating Influxdb jmeter Database"

##Wait until Influxdb Deployment is up and running
##influxdb_status=`kubectl get po -n $tenant | grep perf-test-influxdb | awk '{print $2}' | grep Running

influxdb_pod=`kubectl get po | grep influxdb | awk '{print $1}'`
kubectl exec -ti $influxdb_pod -- influx -execute 'CREATE DATABASE "perf-test"'

## Create the influxdb datasource in Grafana

echo "Creating the Influxdb data source"
grafana_pod=`kubectl get po | grep perf-test-grafana | awk '{print $1}'`

kubectl exec -ti $grafana_pod -- curl 'http://admin:admin@127.0.0.1:3000/api/datasources' -X POST -H 'Content-Type: application/json;charset=UTF-8' --data-binary '{"name":"perf-test","type":"influxdb","url":"http://perf-test-influxdb:8086","access":"proxy","isDefault":true,"database":"perf-test","user":"admin","password":"admin"}'
