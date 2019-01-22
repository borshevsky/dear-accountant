## How to run
echo TLGRM_ACCOUNT='XXX' > env
docker build -t telegram-accountant -f docker/Dockerfile
docker run -it --env-file env telegram-accountant