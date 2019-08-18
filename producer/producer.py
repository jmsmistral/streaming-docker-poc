""" Test data generator for streaming messages to Kafka """

import argparse
import json
import logging
import os
import random
import sys
import time

import hiyapyco
from kafka import KafkaProducer, KafkaClient

import data_generator as dg


logger = logging.getLogger("Main")


def _read_config(config, override):
    # If default config does not exist, try running with overrides
    if not os.path.isfile(config):
        if len(override) == 0:
            raise RuntimeError("No default or override config files provided")

        return hiyapyco.load(override)

    # If no overrides are provided, then use the default config
    if len(override) == 0:
        return hiyapyco.load(config)

    return hiyapyco.load(config, *override, method=hiyapyco.METHOD_MERGE)


def _setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)

    root.addHandler(handler)


def _run_producer_loop(config, producer, topic):
    generator = dg.generator(config)
    # Produce data until stopped by user
    while True:
        message = generator.get_message()
        payload = message.encode()
        try:
            producer.send(topic, value=payload)
        except Error:
            # As this is a PoC we are safely
            # ignoring errors here.
            pass

        logger.info(f"Produced msg: {payload}")

        # Send messages at random intervals
        time.sleep(random.uniform(0.01, config["stream"]["interval"]))


def main(args):
    # Initialize things
    _setup_logging()
    logger.info(f"Args: {args}")
    default_config_path = "./configs/default.yml"
    override_list = []
    if args.override_path is not None:
        override_list = args.override_path.split(",")
    config = _read_config(default_config_path, override_list)
    logger.info(f"Config: {config}")

    # Wait for Kafka to be up and running
    # Note: when running as a service on Docker,
    # it takes some time for the other services
    # like Kafka to start. If we try to establish
    # a connection and produce messages to Kafka
    # before it has started, this producer will
    # crash.
    time.sleep(config["stream"]["wait_for_services"])

    # Create Kafka Producer
    logger.info("Connecting to Kafka")
    logger.info(f"Kafka broker {config['kafka']['broker']}")
    logger.info(f"Kafka broker {config['kafka']['topic']}")

    kafka_broker = KafkaClient(config['kafka']['broker'])
    kafka_producer = KafkaProducer(
        bootstrap_servers=config['kafka']['broker'],
        client_id='test-producer'
    )
    kafka_topic = config['kafka']['topic']

    # Generate data
    logger.info("Starting to produce test data")
    _run_producer_loop(config, kafka_producer, kafka_topic)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate test data for streaming PoC", epilog="Example usage: python producer.py"
    )
    parser.add_argument(
        "--override_path", help="Comma-separated list of overriding config file paths"
    )
    args = parser.parse_args()

    main(args)