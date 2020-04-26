# Team 22 Vehicle Simulator 

This is the vehicle simulator repository for our supply BE testers.

This v-sim will simulate vehicles in our supply BE vehicle database.

## Docker Configuration

### Docker Versioning

Our vehicle simulator image uses the lightweight `3.6-alpine` python image. For more information, please check the [official python alpine repository](https://github.com/docker-library/python/blob/ac47c1bc7bffe22af0c4193f1b1656ca07a24a97/3.6/alpine3.11/Dockerfile). 

### Docker Vehicle Simulator Setup

Please refer to the [official docker docs](https://docs.docker.com/get-docker/) as to installing docker on your computer. 

After setting up docker desktop, you'll be able to pull and run our vehicle simulator application using the following commands:

* `docker pull 42602550/team22:team22vsim`
* `docker run -it --name vsim [imageIdHere] python vehicle_simulator.py`

