from __future__ import unicode_literals

from django.db import models

class Post(models.Model):
    body = models.TextField()
   
    def __unicode__(self):
        return str(self.id)

    def get_excerpt(self, char):
        return self.body[:char]