## Run in docker container
1. build the docker image: `docker build -t elect-gen-core -f .devcontainer/Dockerfile .`
1. run the container: `docker run -p 5801:5801 -v .:/app/data --rm -it elect-gen-core` (it mounts your local directory under `/app/data` in the container, so you can access the files)
1. open browser at http://localhost:5801/ and click `Connect` to connect to the virtual desktop
1. work on the app as usual (you can find your local files under `data/`)
1. closing the app will stop and remove the container or you can remove container manualy
## Instructions to start the algorihtm
1. When launching the application, select Keywords file (.txt) from /app/pystsup/test/acm.txt
1. Then select Students File from /app/data/Students table.xlxs
1. Then secect Course File from /app/data/Course table.xlxs
1. Then select directory where to save the results (.xlxs)
1. Press button "Start Genetic Algorithm" to start algorithm
1. Wait till algorithm stop works (you can monitor the operation of the algorithm in the terminal)
1. Press options to change algorihtm parameters


