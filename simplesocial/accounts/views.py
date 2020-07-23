from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms

# Create your views here.
class SignUp(CreateView):
    """A Class-Based View for User Model signup. Inherits the Django CreateView
    Class-Based View.
    
    Attributes:
        form_class (Class): The ModelForm to link to the SignUp class.
        success_url (str): The route for the client if the form is valid, and
        saved to the database. The Django urls reverse_lazy() function
        is used to prevent the client from taking the route, unless the form
        information is successfully submitted.
        template_name (str): The directory route for the template to be
        displayd by the SignUp Class.
    """
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'