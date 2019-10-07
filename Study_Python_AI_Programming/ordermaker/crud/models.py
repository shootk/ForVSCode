from django.db import models

# Create your models here.


class Message(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"{0}:{1}...".format(self.id, self.message[:10])
