from typing import Any

from django.db import models


class Message(models.Model):
    from_author = models.CharField(max_length=200)
    to_author = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    @staticmethod
    def last_20_messages_from_author_to_author(from_author: str, to_author: str) -> Any:
        messages = Message.objects.raw(
            """SELECT * FROM websocket_message
                        WHERE from_author= %s and to_author=%s or from_author=%s and to_author=%s
                        ORDER BY created_at ASC LIMIT 30""",
            [from_author, to_author, to_author, from_author],
        )
        if len(messages) < 1:
            messages = []
        return messages
