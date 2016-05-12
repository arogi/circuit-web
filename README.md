<b>Running your own Arogi Circuit Router (Traveling Salesman Problem)</b>  
<hr />

*Prerequisites*  

- The router takes a set of GeoJSON point features and returns an ordered set representing the shortest route to travel to them all. The demo comes with a few sample data sets, or you can use your own. You can quickly make your own at: [https://geojson.io](https://geojson.io)

- Install docker. Their webpage has [instructions](https://docs.docker.com/engine/installation/).

- Go to your computer's Terminal shell prompt.

*Getting Started*

1. Type: `docker pull arogi/circuit`  
to grab the latest Arogi docker image. 

2. Start your web browser.

6. Type `localhost`  
in your browser address bar. 

*Shutting Down*  

1. You will need the name of the docker container to shut everything down. To find this, type: `docker ps -a`. Take note of the name; it will be something like *silly_tonsils*

2. Type: `docker stop container_name` to stop docker. Note: You can restart again if you like with `docker start docker_name`

3. To remove the container, type: `docker rm container_name`

4. To remove the image, type: `docker rmi arogi/circuit`
