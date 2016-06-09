<b>Using Docker with Circuit-Web</b>  
<hr />

*Prerequisites*  

 1. Install Docker. Their webpage has [instructions](https://docs.docker.com/engine/installation/).

 2. In Windows and OS X, launch the Docker Quickstart Terminal. Linux uses the standard Terminal.

 3. Make a local copy of arogi-demos. Type:  
    `git clone https://github.com/arogi/circuit-web.git`


*Getting Started*

 1. Type: `docker pull arogi/circuit-web`  
    to grab the latest Circuit-Web Docker image.

 2. Type: `docker run -it -p 80:80 -d -v ~/repos/circuit-web/:/var/www/html arogi/circuit-web`  
    In that statement, replace `~/repos/circuit-web/` with the pathname to your local repository.

 3. Open a web browser and enter the following into the address bar:  
     On OS X and Windows, enter `192.168.99.100`. On Linux, enter `localhost`  


*Running TSP on a Road Network*

 1. Type: `docker pull arogi/arogi-valhalla` to grab the latest Arogi-Valhalla Docker image.
    *Note: This downloads statewide road networks for CA, NV, OR, and AZ. Thus it may take a while, depending on your network speed.*

 2. Type: `docker run -it -d -p 8002:8002 arogi/arogi-valhalla`  

 3. Type `docker ps -a` and check if circuit-web container is still running. If not, do "Getting Started" section above.  

 4. Open a web browser and enter the following into the address bar:  
     On OS X and Windows, enter `192.168.99.100/network.html`. On Linux, enter `localhost/network.html` 


*Shutting Down*  

 1. Return to the Docker terminal.

 2. Type: `docker ps -a`  
    to see a list of all local docker containers. Note the name it gives as a label. It often is something like: `jolly_ptolemy`

 3. To stop Docker, type: `docker stop container_name`

 4. To remove the container, type: `docker rm container_name`

 5. To remove the image, type: `docker rmi image_name` (e.g., `docker rmi arogi/circuit-web`)
