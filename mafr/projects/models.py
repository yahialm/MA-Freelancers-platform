import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from profil.models import CustomUser

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(unique=False, blank=False, max_length=255)
    description = models.TextField(blank=False, null=False)
    demo_link = models.URLField(blank=True)
    github_link = models.URLField(blank=False)
    technologies = ArrayField(models.CharField(max_length=25), max_length=True, default=list)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='projects')

    # Note that the related_name field will allow us to access user's projects in the following way
    # user = CustomUser.object.get(id=1)
    # projects = user.projects.all()

    def __str__(self):
        return self.title