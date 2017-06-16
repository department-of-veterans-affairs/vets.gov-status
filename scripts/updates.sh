#!/usr/bin/env bash

python /application/google_analytics/update_data.py
python /application/google_analytics/update_counts.py

python /application/idme/update_accounts.py

#python /application/prometheus/update_from_prometheus.py

python /application/migration_status_update.py