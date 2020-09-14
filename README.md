# dbpal
An End-to-end Neural Natural Language Interface for Databases implementation based on https://arxiv.org/abs/1804.00401 


# Setting up the local environment and workspace
This guide explains how to set up your environment in order to successfully run the DBpal implementation using the Angular, Django and Docker. It includes information about prerequisites, installing the corresponding parts, and running that app locally to verify your setup. For information of how to install Docker you can check https://docs.docker.com/get-docker/

### Database configuration
In order to have the database ready, we simply need Docker to be installed. After Docker is installed correclty, we need to go to the project directory, open a    powershell or a terminal and do "docker-compose up". That will run the docker-compose.yaml file, where all the configuration is set. 

### UI configuration 

To install Angular on your local system, you need the following:

Node.js: Angular requires a current, active LTS, or maintenance LTS version of Node.js. For information of how to install Node.js you can check https://nodejs.org/en/

npm package manager: Angular applications depend on npm packages for many features. To download and install npm packages, you need an npm package manager. This guide uses the npm client command line interface, which is installed with Node.js by default.

After installing the above mentioned, open a terminal and type: npm install -g @angular/cli
That will install Angular CLI to be available from everywhere. Then one should navigate to the dbpal-ui directory, open a terminal in there and type: npm install .

That will bring all needed npm packages that Angular will use later on. Then we should navigate to the dbpal-ui directory and run: ng serve .

### Django configuration

In order to run Django, we used Anaconda environment with all the needed packages installed. So first, install Anaconda (check guide https://docs.anaconda.com/anaconda/install/) and configure an environment (check guide https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). After your environment is correctly configured, activate it and install the needed packages mentioned here:

1. conda install pytorch torchvision cpuonly -c pytorch
2. conda install -c anaconda django
3. conda install -c conda-forge djangorestframework
4. conda install -c conda-forge django-cors-headers
5. conda install -c auto djangorestframework-jwt
6. conda install -c conda-forge mysqlclient
7. conda install -c conda-forge pymysql 
8. conda install -c conda-forge cryptography
9. conda install -c conda-forge python-jose
10. conda install -c pytorch pytorch 

Next, in that anaconda environment(terminal) navigate to the directory of dbpal and run: python django/manage.py runserver 0.0.0.0:8080 .
That will start the back end service. If you are running Docker in Windows Home and you installed Docker Toolbox on Windows, you should first start the Docker engine
from there, get the IP that will be produced and change from localhost 0.0.0.0 to the IP produced in the file dbpal/django/dbpalproj/settings_dev.py, where it says DATABASES --> HOST (line 98). In this way, the Django will be able to "see" the docker service that is running.

Download the engsql.txt that was used for training from link https://1drv.ms/t/s!AvtMSAl72kBFlXAm2p1baDAM5sKp?e=Gavgfk and place it in the django directory, together with the already existing files encoder.dict and decoder.dict .
When no errors are shown in the terminal where we run the django server, and the the UI part is up(ng serve in the UI configuration), we can navigate to http://localhost:4200/ and start submitting queries.











