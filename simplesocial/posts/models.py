from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
# NOTE: Allows the use of markdowns within posts
import misaka

from groups.models import Group

# Create your models here.
# NOTE: Allows the ability to call things off the current User's session
User = get_user_model()


class Post(models.Model):
    """A class representing a post that a user can make. Inherits the Django
    models.Model class.

    Attributes:
        user (str): Foreign key reference to the user that posted the message.
        created_at (str): Timestamp for post saving to the database.
        message (str): The body of the message being saved to the database.
        message_html (str): A url for the message.
        group (str): Foreign key reference to the group in which the message
        belongs.
    """
    user = models.ForeignKey(User, related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True)

    def __str__(self):
        """String representation of the Post class. Returns the Post's name
        attribute."""
        return self.message

    def save(self, *args, **kwargs):
        """Overwrites the save function to use the misaka library to save
        markup for the message_.html field. Calls the models.Model save
        function."""
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Returns a reverse function that routes the client to the
        posts/single route using the posting User's username and the primary
        key of the post."""
        return reverse('posts:single', kwargs={'username': self.user.username,
                                                'pk': self.pk})

    class Meta:
        """Sets the metadata for the model to order the queried data by the
        created_at attribute in descending order, and create a unique link
        for every message and user."""
        ordering = ['-created_at']
        unique_together = ['user', 'message']