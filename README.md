
# uWSGI Status Check for Datadog

This script provides a custom check for Datadog to monitor the status of uWSGI workers.

## Requirements

- Datadog Agent installed on the machine where uWSGI is running.
- uWSGI running with the stats server enabled (typically on port 1718).
- Install the dependencies from the requirements.txt file.

## Installation

1. Place the `uwsgi_status.py` script in the `/etc/datadog/checks.d/` directory of your Datadog Agent installation.
2. Place the `uwsgi_status.yaml` configuration file in the `/etc/datadog/conf.d/uwsgi_status.d/` directory of your Datadog Agent installation.
3. Restart the Datadog Agent.

## Configuration

In the `uwsgi_status.yaml` file, set the `min_collection_interval` to your desired collection interval in seconds. For a high number of workers, a value of 30 seconds is recommended.

```
init_config:

instances:
  - min_collection_interval: 30  # Set your desired collection interval
```

## Metrics Collected

- `uwsgi.workers.active`: Number of active uWSGI workers.
- `uwsgi.workers.total`: Total number of uWSGI workers.

## Troubleshooting

If you encounter any issues, you can run the check manually:

```
sudo -u dd-agent datadog-agent check uwsgi_status
```

This will provide output on whether the check is running correctly and any metrics it is collecting.

## License

This script is provided under the [MIT License](https://opensource.org/license/mit/).
