from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
	def create_user(self, username, contact, password=None, **extra_fields):
		if not contact:
			raise ValueError('The contact must not be empty')
		user = self.model(username=username, contact=contact, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

class CustomUser(AbstractUser):
	ROLE_CHOICES = [
		('admin','Admin'),
		('user', 'User')
	]
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
	contact = models.IntegerField(max_length=12, )
	def __str__(self):
		return self.username



