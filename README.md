# LocustGraphiteInfluxdb

- Time series database = InfluxDb via Graphite
- Perf test tool = Locust
- Dashboards = Grafana

#### How it works

- On each request / task, post a request to influxdb in graphite format to insert a simple time based metric (e.g. request.1.response.time 100ms <some epoch time>)
- Forms a time series in influxdb
- Datasource created in grafana to peer into influxdb

