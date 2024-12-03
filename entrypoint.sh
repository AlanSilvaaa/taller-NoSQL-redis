#!/bin/sh

if [ "$1" = "data-store" ]; then
    exec python3 examples/data-store/data-store.py
elif [ "$1" = "document-database" ]; then
    exec python3 examples/document-database/document-database.py
else
    echo "Usage: docker run <container> [data-store|document-database]"
    exit 1
fi