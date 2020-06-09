from django.db import models
from ckeditor.fields import RichTextField

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


# CTF challenge categories
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


# CTF challenge difficulties
class Difficulty(models.Model):
    name = models.CharField(max_length=30)
    level = models.IntegerField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.level)

    class Meta:
        verbose_name_plural = 'difficulties'


# CTF challenges
class Challenge(models.Model):
    # Challenge title
    title = models.CharField(max_length=30)
    # Challenge category e.g. Reverse Engineering, Pwn
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Challenge difficulty e.g. Easy, Medium, Hard
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE)
    # Challenge description text
    description = RichTextField()
    # Reward points for solving
    points = models.IntegerField()
    # Fixed point challenge
    is_fixed_point = models.BooleanField(default=True)
    # Min point for dynamic point challenge
    min_points = models.IntegerField(default=0)
    # Penalty for late solvers
    penalty_point = models.IntegerField(default=0)
    # Solver list for current challenge
    solvers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title


# Flags
class Flag(models.Model):
    challenge = models.OneToOneField(Challenge, on_delete=models.CASCADE)
    flag = models.CharField(max_length=256)

    def __str__(self):
        return self.flag


# Solves:
class Solve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


# Player Profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    last_submit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
