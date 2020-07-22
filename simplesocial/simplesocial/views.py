from django.views.generic import TemplateView

# Create your views here.
class HomePage(TemplateView):
    """A TemplateView class for the web application's homepage.

    Attributes:
        template_name (str): The directory path to the template to render for
        the TemplateView.
    """
    template_name = 'index.html'