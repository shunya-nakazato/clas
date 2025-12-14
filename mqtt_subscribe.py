#!/usr/bin/env python3
"""
MQTT Subscriber - Receives messages from MQTT broker
"""

import paho.mqtt.client as mqtt
from mqtt.utils.mqtt import MQTTCallbacks
import logging


def mqtt_subscribe(logger: logging.Logger, broker_host: str, broker_port: int, topic: str, keepalive: int):
    logger.info("=== MQTT Subscriber ===")
    logger.info(f"Connecting to {broker_host}:{broker_port}")

    # Create MQTT client
    client = mqtt.Client(client_id="subscriber_python")

    # Create callback handler with logger
    callbacks = MQTTCallbacks(logger)

    # Set callbacks
    client.on_connect = callbacks.on_connect
    client.on_message = callbacks.on_message
    client.on_disconnect = callbacks.on_disconnect
    client.on_subscribe = callbacks.on_subscribe

    try:
        # Connect to broker
        client.connect(broker_host, broker_port, keepalive=keepalive)

        # Subscribe to topic
        client.subscribe(topic)
        logger.info(f"Subscribed to topic: {topic}")

        # Start the loop to process callbacks
        logger.info("Waiting for messages... (Press Ctrl+C to exit)")
        client.loop_forever()

    except KeyboardInterrupt:
        logger.info("Disconnecting...")
        client.disconnect()
        logger.info("Subscriber stopped")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)
