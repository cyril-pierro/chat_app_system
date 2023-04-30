"""Register all Consumers in the system

This module demonstrates how a list of consumers
subscribe to a particular topic and the operation
performed on that topic

Attributes:
    app_settings (object): Application Settings
    consumer_logger (object): Logger instance
    CLICK_URL (str): Url for verified account
    count (object): Counts the messages sent
"""

import asyncio
import json

from aiokafka import AIOKafkaConsumer
from prometheus_client import Counter

from config import settings
from plugins import mail
from interfaces import consumer
from interfaces import notification as nt
from tools import log

count = Counter(
    name="new_user_messages_sent",  # type: ignore
    documentation="Number of new user messages",
)

app_settings = settings.Settings()

consumer_logger = log.Log(__file__)

CLICK_URL = f"{app_settings.auth_service_url}/api/v1/verify/account"


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
                token = payload.get("token")
                subject = "Welcome to Chat App"
                message = (
                    "Welcome to our Chat Platform,"
                    f"{str(username).capitalize()},"
                    "Click on the link to verify your email \n"
                    f"{CLICK_URL}?token={token}"
                )
                if consume_with is not None:
                    consume_with.send(subject, user_email, message)

        except Exception as e:
            consumer_logger.exception(e.args[0])

        finally:
            await consumer.stop()

    @staticmethod
    def start_process():
        """Start the consumer process"""
        count.inc()
        email_controller = mail.Email()
        asyncio.run(NewUsersConsumer.consume(consume_with=email_controller))
