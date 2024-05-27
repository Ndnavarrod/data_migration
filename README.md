# Code Challenge Solution

## Nelson David Navarro Diaz

For the solution to this challenge, each of the points to be resolved was taken into account, resulting in two main exercises proposed, which in turn lead to three entry points.

1. Carga de Datos
2. Results agregation using  SQL
    - Counts of hired workers by quartes and Job and deparments on 2021.
    - Counts of hired persons by departments on year 2021.

The solution porpose for this challenge Have the next architecture.

<image src="Documentation_images\architecture.png" alt="Descripción de la imagen" caption="Architecture Solution"/>

To execute the solution, it is necessary to have Docker installed as a prerequisite, as everything operates within containers. The entire solution is orchestrated by the Docker Compose file, which initializes the MySQL database in a Docker container that connects to each of the containers for each application. There is one application for each functionality. Therefore, to present the proposed solution from here on, each component will be treated as a separate section.
To inicialice this solution is necessary use >docker-compose build and later run docker-compose up

When the docker star to run this will sho the ip directio to use the entry points having for example

Entry point for load data.
<http://127.0.0.1:5003/load_data>
Entry point for hired by job and deparments by quarter
<http://192.168.0.6:5001/api/data>
Entry point for hired by departments
<http://192.168.0.6:5002/api/data2>

## Mysql Database

The MySQL database is created in the docker-compose.yml file, which is stored in the root directory. We use a MySQL image specifically designed for Docker, simplifying the setup process by providing connection information directly in this file without further complexity.

## Load Data Application

The "Load Data" application is located in the directory named load_data, which consists of the following subfolders and files.

### inputs

This directory contains the CSV files where the information is located to be loaded into the databases.

### Modules

This directory contains modules responsible for specific operations during the data loading process, which are called by other modules or by load_data, which is the main file linked to the entry point.

- table operations: This file contains functions for creating a connection to the database and also for creating tables in the database.
- quality validations: This file contains the input quality validation function, which ensures that each of the input files contains the appropriate columns and values for the assigned table..
- Data import: This file is responsible for uploading the information to the database. It relies on data quality validations and functions with the tables for this purpose.

### Dockerfile

This file creates the Docker image containing the application, installing all the dependent libraries within it to ensure the execution of the app in Docker

### Requirements.txt

It contains the list of libraries to install for the operation of the application.

### load_data.py

This is the file intended to serve as the entry point of the application, which orchestrates the calling of each necessary function in a coordinated manner for the operation's execution. Following the following order:

- Read the argument values from the POST request; if not received, send an error.
- Create a connection with the database.
- Send the parameters to the file loading function, where tables are validated if they exist and created if not, CSV files are read and converted to dataframes, data quality is validated, divided by batch, and loaded into the respective table
- Finally, close the connection.

## Hired by departments and Hired by job and departments

Although these are two different entry points, the directory structure is very similar because their functionality is similar. Therefore, the structure of these directories is very similar, and they will be explained together.

### Templates

This folder contains the tables.html file, which serves as the basis for creating the response in a table format compiled by HTML. It is a basic file since its sole purpose is to be displayed in table format without any real interaction.

### Dockerr file

This file creates the Docker image containing the application, installing all the dependent libraries within it to ensure the execution of the app in Docker

### Requirements.txt

It contains the list of libraries to install for the operation of the application.

### hired_by_**.py

Este archivo contiene la aplicacion como tal lo que hace esta es crear una coneccion con la base de datos, extraer la informacion recibida y ponerla en un formato adecuado,  para asi retornarlar como html compilado con el template, esta utiliza flask para exponer el entry point.

## Migration to Cloud GCP

Given that the application is currently containerized, a simple migration could be done, for example, by creating a virtual machine in Google Cloud Platform's Compute Engine and running everything there. Alternatively, it could be done with a large Docker image in Cloud Build, but this would be a straightforward approach that, while functional, may not provide the best tools or be optimized for this migration. Therefore, since developing this proposal would require time, I will provide two alternative approaches, each starting with different assumptions.

### First Alternative

Consideration: We can connect to the initial MySQL database using a GCP service.

For this alternative, the current database would be connected with the GCP Data Migration Service, which allows us to transfer data to Cloud SQL. This service is chosen considering that the transaction volume for hirings is not very high, and it is a more economical solution than big data options.

Cloud SQL is then connected to BigQuery, solely for analytical tasks such as building views to feed the dashboards, which would be the equivalent of the current entry points. To stay within the same provider and facilitate connections, the output tables are created as Looker dashboards. This would allow users to have additional filters and better visualize the information, as well as the inclusion of graphs
<image src="Documentation_images\FirstAlternative.png" caption="Architecture Solution First alterntative"/>

### Second Alternative

Consideration: The migration is only with csv files.

For this second alternative, considering that it can only be done with files, the aim is to create a bucket that contains the CSV files. For the application, a Cloud Run can be used that would utilize the same load data function already created and store it in the Cloud SQL database. This data can then be consumed by BigQuery for analysis and Looker dashboards.

<image src="Documentation_images\SecondAlternative.png" caption="Architecture Solution First alterntative"/>
