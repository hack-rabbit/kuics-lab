from django.views.generic.base import TemplateView

from registration.backends.default.views import RegistrationView, ActivationView
from config.forms import RegisterForm


# Homepage
class HomeTV(TemplateView):
    template_name = 'home.html'


# Registration
class RegisterRV(RegistrationView):
    template_name = 'registration/registration_form.html'
    form_class = RegisterForm
    #success_url = 'registration/registration_complete.html'


class RegisterDoneTV(TemplateView):
    template_name = 'registration/registration_complete.html'


class ActivateAV(ActivationView):
    template_name = 'registration/activate.html'


class ActivateDoneTV(TemplateView):
    template_name = 'registration/activation_complete.html'
