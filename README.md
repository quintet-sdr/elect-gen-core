## Run in docker container
1. build the docker image: `docker build -t elect-gen-core -f .devcontainer/Dockerfile .`
1. run the container: `docker run -p 5801:5801 -v .:/app/data --rm -it elect-gen-core` (it mounts your local directory under `/app/data` in the container, so you can access the files)
1. open browser at http://localhost:5801/ and click `Connect` to connect to the virtual desktop
1. work on the app as usual (you can find your local files under `data/`)
1. closing the app will stop and remove the container or you can remove container manualy

