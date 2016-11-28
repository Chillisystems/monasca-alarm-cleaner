# Monasca alarm cleaner

This tool will clean leftover alarms from monasca after vm removal. This will work only for
alarms whith _resource_id_ defined. So best option is add _resource_id_ entry to your
monasca agent _agent.yaml_


## Monasca Agent Configuration

```
Api:
  amplifier: 0
  backlog_send_rate: 1000
  ca_file: null
  insecure: false
  keystone_url: {{ mon_agent_keystone_url }}
  max_buffer_size: 1000
  password: {{ mon_agent_pass }}
  project_domain_id: null
  project_domain_name: {{ mon_agent_project_domain_name }}
  project_id: null
  project_name: {{ mon_agent_project }}
  url: {{ mon_agent_api_url }}
  user_domain_id: null
  user_domain_name: {{ mon_agent_user_domain_name }}
  username: {{ mon_agent_admin }}
Logging:
  collector_log_file: /var/log/monasca/agent/collector.log
  forwarder_log_file: /var/log/monasca/agent/forwarder.log
  log_level: INFO
  statsd_log_file: /var/log/monasca/agent/statsd.log
Main:
  check_freq: 30
  collector_restart_interval: 24
  dimensions:
    service: monitoring
    resource_id {{ virtual_machine_id }}
  hostname: {{ inventory_hostname }}
  sub_collection_warn: 5
Statsd:
  monasca_statsd_port: 8125

```

## TODO

    * Add tests