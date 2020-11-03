from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass

class Listing():
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=2000)
	starting_bid = models.FloatField()
	image = models.ImageField(null=True)

	def __str__(self):
		return f"{self.title}: {self.current_bid}"

