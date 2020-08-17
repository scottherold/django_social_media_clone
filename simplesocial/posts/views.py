from django.contribu.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms, models

# Create your views here.

# NOTE: Extracts User model from the session
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    """Class for a list of posts tied to a group.

    Attributes:
        model (Class): The name of the class that is used to instantiate data
        to the view.
        selected_related (tup): The models related to the linked Post model.
    """
    model = models.Post
    select_related = ('user', 'group')


class UserPosts(generic.ListView):
    """Class for posts a specific user has made.

    Attributes:
        model (Class): The name of the class that is used to instantiate data
        to the view.
        template_name (str): The URL for the template to be produced by the
        view.
    """
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        """Returns the user's posts and sets the class attribute post_user if
        the user exists and the posts tied to that user if they can be fetched.
        Raises a Http404 otherwise."""
        try:
            self.post.user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else: 
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        """Returns context after adding the key/value pair 'post_user' from
        the class attribute 'post_user'."""
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    """Class for a specific post.

    Attributes:
        model (Class): The name of the class that is used to instantiate data
        to the view.
        template_name (str): The URL for the template to be produced by the
        view.
    """
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        """Returns the queryset for the model if the related user model is the
        same as the username for the post."""
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    """A class representing a form submission to generate a new post.

    Attributes:
        fields (tup): The allowable editable fields by the user.
        model (Class): The model class to link the form data.
    """
    fields = ('message', 'group')
    model = models.Post

    def form_Valid(self, form):
        """Returns a boolean if the form is valid. Saves the information to the
        database if the form is valid."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    """A class representing a view to delete a post.

    Attributes:
        fields (tup): The allowable editable fields by the user.
        model (Class): The model class to link the form data.
    """
    fields = ('message', 'group')
    model = models.Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        """Returns the queryset for the model if the related user model is the
        same as the username for the post."""
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self, *args, **kwargs):
        """Returns the DeletePost class delete method. Appends a message to the
        method, declaring the post has been delete."""
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)