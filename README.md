# salv.ia

To run SalvIA on your cloud in Docker:

0. mkdir huggingface_models

1. docker build . -t salvia
   
2. docker run --gpus all -e BOT_TOKEN=<your telegram token> -m 25g --memory-swap 28g  -v ./huggingface_models:/opt/dlami/nvme/huggingface_cache salvia