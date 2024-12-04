#!/bin/sh

FOLDER=$1
ACTION=$2

if [ "$FOLDER" = "document-database" ]; then
    if [ "$ACTION" = "create" ]; then
        exec python3 examples/document-database/create.py
    elif [ "$ACTION" = "query" ]; then
        exec python3 examples/document-database/query.py
    else
        echo "Unknown action: $ACTION. Use 'create' or 'query'."
        exit 1
    fi
elif [ "$FOLDER" = "data-store" ]; then
    if [ "$ACTION" = "create" ]; then
        exec python3 examples/data-store/create.py
    elif [ "$ACTION" = "query" ]; then
        exec python3 examples/data-store/query.py
    else
        echo "Unknown action: $ACTION. Use 'create' or 'query'."
        exit 1
    fi
else
    echo "Unknown folder: $FOLDER. Use 'document-database' or 'data-store'."
    exit 1
fi
