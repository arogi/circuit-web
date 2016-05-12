<b>Running your own Arogi Circuit Router (Traveling Salesman Problem)</b>  
<hr />

*Prerequisites*  

- The router takes a set of GeoJSON point features and returns an ordered set representing the shortest route to travel to them all and return. This implementation uses straightline distance, but we are open to adding street route distance too. The demo comes with a few sample data sets, or you can use your own. You can make your own at: [https://geojson.io](https://geojson.io).

- Install docker. Their webpage has [instructions](https://docs.docker.com/engine/installation/).

- Go to your computer's Terminal shell prompt.

*Getting Started*

1. Type: `docker pull arogi/circuit`  
to grab the latest Arogi docker image. 

2. Start your web browser.

6. Type `localhost`  
in your browser address bar. 

*Shutting Down*  

1. You will need the name of the docker container to shut everything down. To find this, In your Terminal shell, type: `docker ps -a`. Take note of the name; it will be something like *silly_tonsils*. For the rest of the steps, use the name wherever it says `container_name`

2. Type: `docker stop container_name` to stop docker. Note: You can restart again if you like with `docker start container_name`

3. To remove the container, type: `docker rm container_name`

4. To remove the image, type: `docker rmi arogi/circuit`

*Limits*

* None, actually. Via Docker, the whole thing is running on your hardware, so you can add as many points as you can stand. On our individual laptops, 100 points loads immediately; 500 takes about xxx seconds, and 5000 takes xxx seconds.

* Arogi Circuit is free and open source. Arogi code is under the Apache 2.0 License. We use a smattering of other open source libraries too, and you will find credits to them in the code-- particular thanks to Google, Mapzen, and Leaflet.

Enjoy!
