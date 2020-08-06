from django import template
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
# NOTE: Allows the use of markdowns within posts
import misaka

# Create your models here.
# NOTE: Allows the ability to call things off the current User's session
User = get_user_model()

# NOTE: This is how to use custom template tags
register = template.Library()


class Group(models.Model):
    """A class representing a group that a user can join. Inherits the Django
    models.Model class.

    Attributes:
        name (str): The name of the Group. Limited to 255 characters.
        slug (str): The name of the Group slugged (lowercased, and hyphens for
        whitespace).
        description (str): The group's description.
        description_html (str): A url for the group's description.
        members (list): A list of users (User Model) for the Group as a
        many-to-many relationship with the GroupMember Class.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        """String representation of the Group class. Returns the Group's name
        attribute."""
        return self.name

    def save(self, *args, **kwargs):
        """Overwrites the save function to slugify the Group's name attribute
        as the slug attribute and uses the misaka library to save markup for
        the description_html field. Calls the models.Model save function."""
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns a reverse function that routes the client to the Group name
        route using the Group's slug attribute."""
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        """Sets the metadata for the model to order the queried data by the
        name attribute."""
        ordering = ['name']

class GroupMember(models.Model):
    """A class representing the membership of a User model to a group. Inherits
    the Django models.Model class.

    Attributes:
        group (str): The group that the GroupMember belongs. Has a foreign
        key relationship with a Group model.
        user (str): The User linked to the GroupMember model. Has a
        foreign key relationship with a User model.
    """
    group = models.ForeignKey(Group, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_groups')

    def __str__(self):
        """String representation of the GroupMember class. Returns the username
        attribute from the related User model, using the GroupModel user
        attribute"""
        return self.user.username

    class Meta:
        """Settings for the GroupMember class.

        Attributes:
            unique_together (tuple): Establishes a many-to-many relationship
            using the GroupMember class's related Models through its
            group and user attributes.
        """
        unique_together = ('group', 'user')