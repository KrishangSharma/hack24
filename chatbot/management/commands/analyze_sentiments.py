from django.core.management.base import BaseCommand
from textblob import TextBlob
from chatbot.models import Chat

class Command(BaseCommand):
    help='Analyzes sentiment of chat messages'

    def handle(self, *args, **kwargs):
        messages=Chat.objects.all()

        for message in messages:
            sentiment=TextBlob(message.message).sentiment.polarity

            message.sentiment_score=sentiment
            message.save()

            self.stdout.write(self.style.SUCCESS(f'Analyzed message {message.sentiment_score}'))