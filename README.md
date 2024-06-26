## Run in docker container
1. clone this repository: `git clone https://github.com/LCAS/pareto-optimal-student-supervisor-allocation.git`
1. build the docker image: `docker build -t pareto-optimal-student-supervisor-allocation -f .devcontainer/Dockerfile .`
1. run the container: `docker run -p 5801:5801 -v .:/app/data --rm -it pareto-optimal-student-supervisor-allocation` (it mounts your local directory under `/app/data` in the container, so you can access the files, e.g. your student and supervisor Excel sheets)
1. open browser at http://localhost:5801/ and connect to the virtual desktop
1. work on the app as usual (find your local files under `data/`)
1. closing the app will stop and remove the container