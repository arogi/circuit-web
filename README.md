**status: 15 May 2016 -- @glennon and @LEDominator are prepping the Docker image. This line will be removed when it is operational.**  

<b>Running your own Arogi Circuit Router (Traveling Salesman Problem)</b>  
<hr />

*Prerequisites*  

- Arogi Circuit takes a set of GeoJSON point features and returns an ordered set representing the shortest route to travel to them all and return. For now, this implementation uses straightline, Euclidean, distance. The demo comes with a few sample data sets, or you can use your own. You can make your a GeoJSON with: [https://geojson.io](https://geojson.io).

- Place your GeoJSON file in a folder such as ~/data/ and rename it `mydata.geojson`.

- We have bundled all the code to make Arogi Circuit work in a Docker container, so go install Docker. Their webpage has [instructions](https://docs.docker.com/engine/installation/).

- Open your computer's Terminal shell prompt.

*Getting Started*

1. Type: `docker pull arogi/circuit-web`  
to grab the latest Arogi docker image.  

2. Type: `docker run -it -p 80:80 -v ~/data/:/var/www/html/data arogi/circuit-web`  
to run Docker and have it find your data in the ~/data directory.

3. Start your web browser.

4. Type `localhost`  
in your browser address bar.  

*Shutting Down*  

1. You will need the name of the docker container to shut everything down. To find this, In your Terminal shell, type: `docker ps -a`. Take note of the name; it will be something like *silly_tonsils*. For the rest of the steps, use the name wherever it says `container_name`

2. Type: `docker stop container_name` to stop docker. Note: You can restart again if you like with `docker start container_name`

3. To remove the container, type: `docker rm container_name`

4. To remove the image, type: `docker rmi arogi/circuit`

*Limits*

* The map control and data use online sources; otherwise, via Docker, the whole thing is running on your hardware. You can add as many points as you can stand. On a normal, medium-slow laptop, 100 points load immediately; 500 take about 8 seconds, and 1000 take 45 seconds.

* Arogi Circuit is free and open source. Arogi code is under the Apache 2.0 License. We use a smattering of other open source libraries too, and you will find credits to them in the code-- particular thanks to Google, Mapzen, and Leaflet.

Enjoy!

![Screenshot](https://raw.githubusercontent.com/arogi/circuit-web/master/images/tangle2.png)
