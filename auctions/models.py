from django.contrib.auth.models import AbstractUser
from django.db import models

#References the name 'Listing' instead of the model itself since
#model isn't defined yet
class User(AbstractUser):
    watch_list = models.ManyToManyField('Listing', blank=True, related_name="watchers")

class Listing(models.Model):
	title = models.CharField(max_length = 128)
	description = models.CharField(max_length = 4000)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
	starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
	#image = models.FileField(blank = True, upload_to='uploads/')
	image = models.FileField(upload_to='uploads/', verbose_name='image')
	category = models.CharField(max_length = 64, blank = True)

	def __str__(self):
		return f"{self.title}"

class Bid(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
	bid = models.DecimalField(max_digits=8, decimal_places=2)

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
	comment = models.CharField(max_length=2000)

	def __str__(self):
		return f"{self.user.username} - {self.comment}"