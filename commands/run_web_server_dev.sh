#!/bin/sh
# Run migrations before starting the server
/app/commands/run_migration.sh

# Start the development server
echo "Starting development server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
