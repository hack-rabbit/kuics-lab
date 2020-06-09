from django.urls import path
from django.conf.urls import handler404


from ctf import views

app_name = 'ctf'
urlpatterns = [
    # CTF Challenges List
    path('list/', views.ChallengeLV.as_view(), name='list'),
    # Challenge details
    path('list/<int:pk>/', views.ChallengeDV.as_view(), name='detail'),
    # Flag Authentication
    path('list/<int:challenge_id>/submit/', views.authenticate, name='submit'),
    # Leaderboard
    path('leaderboard/', views.LeaderboardLV.as_view(), name='leaderboard'),
]

# Errors
handler404 = 'ctf.views.error_404'