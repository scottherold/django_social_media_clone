from django.db import models
from django.contrib import auth

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    """A Model class for a User. Inherits the Django auth User Model class
    and the Django auth PermissionsMixin."""

    def __str__(self):
        """String representation of the User Model using the inherited username
        attribute from the Django auth User Model class."""
        return "@{}".format(self.username)