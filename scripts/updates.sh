#!/usr/bin/env bash

cd google_analytics
python update_data.py
python update_counts.py

cd ../idme
python update_accounts.py

cd ../prometheus
python update_from_prometheus.py
