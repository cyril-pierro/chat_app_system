"""Register all Consumers in the system

This module demonstrates how a list of consumers
subscribe to a particular topic and the operation
performed on that topic

Attributes:
    app_settings (object): Application Settings
    consumer_logger (object): Logger instance 
"""

import asyncio
import json

from aiokafka import AIOKafkaConsumer

from config import settings
from controller import mail
from interfaces import consumer
from interfaces import notification as nt
from tools import log

app_settings = settings.Settings()

consumer_logger = log.Log(__file__)


class NewUsersConsumer(consumer.NotificationConsumer):
    """Consumer for New Users in the System

    This class describes the operations performed
    for users that just joined the system
    """
    @staticmethod
    async def consume(consume_with: nt.NotificationController = None):
        """Listen to a particular topic

        Args:
            consume_with (class): The operation controller 
                The controller to use when you are listening
                to a particular topic
        """
        consumer = AIOKafkaConsumer(
            app_settings.topic_to_listen_on,
            bootstrap_servers=app_settings.broker_url,
            group_id=app_settings.consumer_group_id,
        )

        await consumer.start()
        try:
            async for msg in consumer:
                payload = json.loads(msg.value)
                username = payload.get("username")
                user_email = payload.get("email")
                subject = "Welcome to Chat App"
                message = f"Welcome to our family {str(username).capitalize()}"
                if consume_with is not None:
                    consume_with.send(subject, user_email, message)

        except Exception as e:
            consumer_logger.exception(e.args[0])

        finally:
            await consumer.stop()

    @staticmethod
    def start_process():
        """Start the consumer process
        """
        email_controller = mail.Email()
        asyncio.run(NewUsersConsumer.consume(consume_with=email_controller))
