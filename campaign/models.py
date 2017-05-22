# python imports
import uuid
import os

# django imports
from django.db import models
from django.utils import timezone
from .choices import CATEGORY_CHOICES

#local imports


def get_maillistFile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('excels/', filename)


def get_templatesfile_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('templates/', filename)


def get_templatesimage_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)


class MailingList(models.Model):
	mail_list_name = models.CharField(max_length = 50)
	user = models.ForeignKey('auth.User')
	file = models.FileField(upload_to = get_maillistFile_path)
	added_date = models.DateTimeField(default = timezone.now)

	def __str__(self):
		return self.mail_list_name


class Template(models.Model):
	image = models.ImageField(upload_to=get_templatesimage_path, null = True)
	template_name = models.CharField(max_length = 50, unique = True)
	template_image = models.ImageField(upload_to = get_templatesimage_path)
	file = models.FileField(upload_to = get_templatesfile_path)
	category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, null=False)

	def __str__(self):
		return self.template_name


class UserCampaign(models.Model):
	campaign_name = models.CharField(max_length = 50, unique = True)
	user = models.ForeignKey('auth.User')
	created_date = models.DateTimeField(default = timezone.now)
	mail_list = models.ForeignKey(MailingList)
	template = models.ForeignKey(Template)

	def __str__(self):
		return self.campaign_name

