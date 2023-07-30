
## before start, run this command to create a docker network, flask project and postgresql database will run in the same network
docker network create my_network


# Flask project

## step 1, build docker image
docker build -t my6400 .

## step 2, run docker image
docker run --name my_flask_app --network my_network -p 5000:5000 my6400

## step 3, check the main page using the following link
http://127.0.0.1:5000


# Database

## step 1, pull postgres image in local
docker pull postgres:latest

## step 2, run the image
docker run -d --name my_postgres_db -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase --network my_network -p 5432:5432 postgres:latest

## step 3, check your database host IP address using this command
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [your container id]

## step 4, with the IP in step 3, you can setup your database connection in software like Dbeaver, DataGrip, etc.