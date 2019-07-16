# Dojo Twitter Stream

This project contains an application for capture Twitter posts by Twitter Stream API and a small Java Reactive API for 
integration with AWS Comprehend.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Docker Comunity Edition - 2.0.0.3 (https://docs.docker.com/install)
Docker Compose (https://docs.docker.com/compose/install/)
Java 8 (https://www.java.com/pt_BR/download/)
Apache Maven 3.6.1 (https://maven.apache.org/download.cgi)
```

### Installing

A step by step series of examples that tell you how to get a development env running

#### Running the Database and Twitter Collector Containers

The database and collector app are conteinerized at the docker-compose.yml file. To run those apps, you should execute:

```
docker-compose up -d
```

After that, you will should have two containers running: A MongoDB document database and a Python collection worker. To check it out, run the command:

```
docker-compose ps
```
#### Running the Reactive API

In order to run the Java Reactive API:

```
cd TwitterRxApi
mvn spring-boot:run
```

After that, you should be able to request some data from the api like that

```
curl localhost:5000/tweets
```

With a twitter post in hands, now you can interact with the amazon comprehend capabilities. 
In order to extract entities from the text, you can call the api like that:


```
curl localhost:5000/tweets/{id}/comprehend-entities
```

With a twitter post in hands, now you can interact with the amazon comprehend capabilities. 
In order to extract sentiment from the text, you can call the api like that:


```
curl localhost:5000/tweets/{id}/comprehend-sentiment
```

With a twitter post in hands, now you can interact with the amazon comprehend capabilities. 
In order to extract key phrases from the text, you can call the api like that:


```
curl localhost:5000/tweets/{id}/comprehend-keyphrases
```

## Deployment

To Be Defined

## Built With

* [SpringBoot] (https://spring.io/projects/spring-boot) - Used to develop the Rest API
* [WebFlux] (https://projectreactor.io/) - Reactive Extensions
* [Python 3.6) (https://www.python.org/) - Programming languange applied at Collector Worker
* [Tweepy] (https://www.tweepy.org/) - Python twitter wrapper
* [MongoDB] (https://www.mongodb.com/) - Document Database
* [Maven] (https://maven.apache.org/) - Dependency Management
* [AWS Java SDK] (https://aws.amazon.com/pt/sdk-for-java/) - AWS Services Integration

## Contributing

To be defined

## Versioning

To be defined

## Authors

* **Marku Vinícius** - *Initial work* - [markuvinicius](https://github.com/markuvinicius)

To be defined

## License

To be defined

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
