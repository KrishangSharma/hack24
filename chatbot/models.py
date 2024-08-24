from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    STATUS_CHOICES=(
        ('new', 'New'),
        ('resolved', 'Resolved'),
        ('pending', 'Pending'),
    )
    CATEGORY_CHOICES=[
        ('Transport', 'Transport'),
        ('Education', 'Education'),
        ('Security', 'Security'),
        ('Public Service', 'Public Service'),
        ('Sanitation', 'Sanitation'),
        ('Environment', 'Environment'),
        ('Health', 'Health'),
        ('Services', 'Services'),
        ('Housing', 'Housing'),
        ('Infractructure', 'Infractructure'),
        ('Jobs', 'Jobs'),
        ('Sports', 'Sports')
    ]
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    message=models.TextField()
    category=models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    response=models.TextField(default="I am sorry. I dont understand your question") 
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True )
    resolved_at = models.DateTimeField(null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    classification=models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}:{self.message}:{self.sentiment_score}:{self.created_at}:{self.category}'
    
    def sentiment_status(self):
        if self.sentiment_score is not None:
            if self.sentiment_score>0.1:
                return "Positive"
            elif self.sentiment_score<-0.1:
                return "Negative"
            else:
                return "Neutral"
        return "Unknown"
   

    
# class Sentiment(models.Model):
#     chat = models.ForeignKey(Chat, related_name='sentiments', on_delete=models.CASCADE, null=True)
#     score=models.FloatField()
#     created_at=models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.chat.user.username} at {self.created_at}:{self.score}'
    
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    sub_county=models.CharField(max_length=100)
    ward=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

