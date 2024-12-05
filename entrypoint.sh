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
    elif [ "$ACTION" = "delete" ]; then
        exec python3 examples/data-store/delete.py
    elif [ "$ACTION" = "update" ]; then
        exec python3 examples/data-store/update.py
    elif [ "$ACTION" = "read" ]; then
        exec python3 examples/data-store/read.py
    else
        echo "Unknown action: $ACTION. Use 'create', 'delete', 'update' or 'read'."
        exit 1
    fi
elif [ "$FOLDER" = "vector-database" ]; then
    if [ "$ACTION" = "create" ]; then
        exec python3 examples/vector-database/create.py
    elif [ "$ACTION" = "query" ]; then
        exec python3 examples/vector-database/query.py
    else
        echo "Unknown action: $ACTION. Use 'create', 'delete', 'update' or 'read'."
        exit 1
    fi
else
    echo "Unknown folder: $FOLDER. Use 'document-database', 'vector-database' or 'data-store'."
    exit 1
fi
