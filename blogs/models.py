from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
	"""Topic of blog post"""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		"""Return a string representation of the model."""
		return self.text

class Entry(models.Model):
	"""Entry for blog post"""
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta: verbose_name_plural = 'entries'

	def __str__(self): 
		"""Return string representation of model"""
		text = self.text
		big_text = self.text[:50]
		if text > big_text:
			return big_text + "..."
		else:
			return text