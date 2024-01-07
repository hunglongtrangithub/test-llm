#!/bin/bash

# Start the controller
python3 -m fastchat.serve.controller &

# Start the model workers for each of the three vicuna models
# Note: Replace 'vicuna-model1', 'vicuna-model2', and 'vicuna-model3' with the actual model paths
python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5-16k &
python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-13b-v1.5-16k &
python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-33b-v1.3 &

# Start the RESTful API server
python3 -m fastchat.serve.openai_api_server --host localhost --port 8000 &
