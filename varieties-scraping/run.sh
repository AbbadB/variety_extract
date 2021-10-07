#!/bin/bash

docker pull abbadb/ubuntu_infra:latest
docker run -v $(pwd):/app -e USE_PROXY=False abbadb/ubuntu_infra python3 /app/variety-links-scraping.py
csvfile=$(ls link*.csv | head -n1)
docker run -v $(pwd):/app -e USE_PROXY=False abbadb/ubuntu_infra python3 /app/variety-scraping.py -i /app/$csvfile
