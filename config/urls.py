from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView
from config.views import HomeTV, RegisterRV, RegisterDoneTV, ActivateAV, ActivateDoneTV
from config.forms import LoginForm

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Homepage
    path('', HomeTV.as_view(), name='home'),

    # Authentication
    path('accounts/login/', LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('accounts/logout', LogoutView.as_view(), name='logout'),

    # Registration
    path('accounts/register/', RegisterRV.as_view(), name='registration'),
    path('accounts/register/complete/', RegisterDoneTV.as_view(), name='registration_complete'),
    path('accounts/activate/complete/', ActivateDoneTV.as_view(), name='registration_activation_complete'),
    path('accounts/activate/<str:activation_key>/', ActivateAV.as_view(), name='registration_activate'),

    # CTF Application
    path('wargame/', include('ctf.urls')),
]
