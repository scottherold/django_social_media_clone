from django.contrib import messages
from django.contrib.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from groups.models import Group, GroupMember


# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    """A CreateView class for a specific Group model data object. This class
    utlizes the LoginRequiredMixin to authenticate a User prior to allowing
    write access to the database.

    Attributes:
        fields (tuple): fields in the linked model the logged in User is able
        to edit through a client form.
        model (Class): Links the the client form fields to the Group model
        attributes.
    """
    fields = ('name', 'description')
    model = Group


class SingleGroup(generic.DetailView):
    """A DetailView class for a specific Group model data object.

    Attributes:
        model (Class): Links the the client form fields to the Group model
        attributes.
    """
    model = Group


class ListGroups(generic.ListView):
    """A ListView Class for a list of Group model objects in the database.
    
    Attributes:
        model (Class): Links the the client form fields to the Group model
        attributes.
    """
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    """A RedirectView Class for a user joining a group."""

    def get_redirect_url(self, *args, **kwargs):
        """Returns a reverse call to the SingleGroup class using the group's
        slug as a path string."""
        return reverse('groups:single', kwargs={ 'slug': self.kwargs.get('slug') })

    def get(self, request, *args, **kwargs):
        """Returns the parent get method, creating a new member in a group with
        the authenticated user. Attaches an error message if the user is
        already a member of the group, or a success message if the user is
        added to a new group."""
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.object.create(user=self.request.user, group=group)
        except:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    """A RedirectView Class for a user leaving a group."""

    def get_redirect_url(self, *args, **kwargs):
        """Returns a reverse call to the SingleGroup class using the group's
        slug as a path string."""
        return reverse('groups:single', kwargs={ 'slug': self.kwargs.get('slug') })

    def get(self, request, *args, **kwargs):
        """Returns the parent get method, deleting the authenticated user from
        the group. Attaches an error message if the user is not a member of the
        group, or a success message if the user is deleted from the group."""

        try:
            membership = GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, "Sorry you aren't in this group!")
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')

        return super().get(request, *args, **kwargs)