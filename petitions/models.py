from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    id = models.AutoField(primary_key=True)

    # Movie stored as a simple text field and must be present and unique
    movie_name = models.CharField(max_length=255, unique=True)

    # Creator must be set (no anonymous creators)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_petitions")

    # Signers: many-to-many to users (no timestamp). Keep blank=True so petition can start empty.
    signers = models.ManyToManyField(User, blank=True, related_name="signed_petitions")

    def __str__(self):
        return f"{self.movie_name} — {self.signers.count()} signatures"
