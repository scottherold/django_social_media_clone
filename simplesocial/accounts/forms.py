from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# Create your forms here.

# NOTE: When inheriting from django libraries, ensure that the class names are
# not the same as the inheritied django library names.
class UserCreateForm(UserCreationForm):
    """A Model Form for User Model 'create' procedure. Inherits the Django auth
    UserCreationForm Model Form."""

    class Meta:
        """Meta class for UserCreateForm ModelForm Class settings.

        Attributes:
            fields (tuple): A tuple of fields to map to the client.
            model (Class): The Model to map to the Model Form. The Django auth
            get_user_model() function is provided to automatically map to the
            Django auth User Model.
        """
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        """Instantiation options for UserCreateForm ModelForm Class. Used to 
        transform labels for mapped fields in Meta."""
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'