<b>Arogi Circuit Router Quickstart</b>
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

Want to use your own data? [Easy!](https://github.com/arogi/circuit-web/blob/master/README.md)  

Screenshot:  
![Screenshot](https://raw.githubusercontent.com/arogi/circuit-web/master/images/quickstart-screenshot.png)
