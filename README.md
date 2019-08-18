# Data Streaming PoC with Kafka, Spark, and Zeppelin #

Here you'll find a small proof-of-concept for how to:
* Generate semi-realistic, synthetic data through a config-driven Python app
* Send JSON messages through a Kafka message broker
* Process streaming data with Spark on Zeppelin notebooks (including window funtions)

## How to run ##

* Dependencies: docker, docker-compose
* Requirements: You *might* need to increase the memory assigned to Docker to ~8GB

Clone the repo, navigate to the directory, and run:

```bash
$ docker-compose up
```

This will bring up:
* Python test data generation app (this will sleep for 20 seconds waiting for Kafka to be up before producing data)
* Kafka (with Zookeeper as a separate service)
* Zeppelin (already configured with everything needed to analyse Kafka streams with Spark)

Then navigate to: `localhost:8080` to access Zeppelin