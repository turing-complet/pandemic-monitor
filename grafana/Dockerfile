FROM grafana/grafana

COPY datasources.yaml /etc/grafana/provisioning/datasources/
COPY dashboards.yaml /etc/grafana/provisioning/dashboards/
COPY *.json /var/lib/grafana/dashboards/