from django.contrib.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.shortcuts import render
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