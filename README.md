# prometheus-stdin-metric-collector

This is a tool that collects metrics from stdin and 
makes them scrapable for [Prometheus](https://prometheus.io/).
The metric must have custom timestamp.

The input metrics must be in the following format:
```
ts:<TIMESTAMP> <METRIC_NAME>:<VALUE> <ANOTHER_METRIC_NAME>|<TAG>:<VALUE>...
```


## Usage

To run the tool that reads from stdin:
```
python prometheus-stdin-metric-collector.py
```

This tool can be used to supply metrics to Prometheus
from an application that dumps its metrics into a log file.

For example, to continuously read the log:

```
tail -f <LOG_FILE> | python prometheus-stdin-metric-collector.py
```

The [prometheus-stdin-metric-collector.service](prometheus-stdin-metric-collector.service) file can be used as an example
how to wrap a command/script as a systemd service.

## Dependencies

* Python 3.6
* prometheus-client: `pip install prometheus-client`
