from django.db import models
from .choices import PACKAGE_CHOICES



class UserProfile(models.Model):
	user = models.ForeignKey('auth.User')
	sent_email = models.IntegerField(default = 0)
	remaining_email = models.IntegerField(default = 0)
	business_name = models.CharField(max_length = 100, null = True)
	package = models.CharField(max_length = 10, choices = PACKAGE_CHOICES, default = 'BASIC')
	email = models.EmailField()



