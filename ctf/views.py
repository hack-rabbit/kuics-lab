from django.shortcuts import render, redirect
from django.template import RequestContext

from django.views.generic import ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q

from django.utils import timezone

from django.contrib.auth.models import User
from ctf.models import Challenge, Difficulty, Profile, Solve

from django.http import HttpResponseRedirect


# ListView
class ChallengeLV(LoginRequiredMixin, ListView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super(ChallengeLV, self).get_context_data(*args, **kwargs)
        difficulty_list = Difficulty.objects.all().order_by('level')
        
        context['challenge_list_all'] = dict()
        for d in difficulty_list:
            context['challenge_list_all'][d.name] = Challenge.objects.filter(Q(difficulty=d)).order_by('points')

        return context


class LeaderboardLV(LoginRequiredMixin, ListView):
    model = Profile

    def get_queryset(self):
        return Profile.objects.order_by('-score')


# DetailView
class ChallengeDV(LoginRequiredMixin, DetailView):
    model = Challenge


# Function-based View
def authenticate(request, challenge_id):
    flag = request.POST.get('flag', None)
    user_id = request.POST.get('user_id', None)

    challenge = Challenge.objects.get(pk=challenge_id)

    # Already solved by requesting user
    for solver in challenge.solvers.all():
        if str(user_id) == str(solver.id):
            return HttpResponseRedirect(reverse('ctf:list'))

    # Flag check
    if str(flag) == str(challenge.flag):
        user = User.objects.get(pk=user_id)
        # Add score
        user.profile.score += challenge.points
        # Decrease points for dynamic challenge
        if not challenge.is_fixed_point:
            if challenge.points > challenge.min_points:
                challenge.points -= challenge.penalty_point;
        # Add challenge to challenge_set
        user.challenge_set.add(challenge)
        # Commit changes
        user.save()
        challenge.save()
        solve = Solve.objects.create(user=user, challenge=challenge)
        return HttpResponseRedirect(reverse('ctf:list'))
    else:
        return HttpResponseRedirect(reverse('ctf:list'))

# Error
def error_404(request, exception):
    return render(request, '404.html', status=404)
