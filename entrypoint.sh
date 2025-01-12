# entrypoint.sh

#!/bin/bash

# Start MeiliSearch
./meilisearch --master-key="$MEILISEARCH_MASTER_KEY" &

# Start FastAPI with Uvicorn
uvicorn main:app --host $FASTAPI_HOST --port $FASTAPI_PORT &

# Start Gradio
python frontend/gradio_app.py --server_name $GRADIO_HOST --server_port $GRADIO_PORT &

# Wait for all background processes to finish
wait -n

# Exit with status of the first process to exit
exit $?
