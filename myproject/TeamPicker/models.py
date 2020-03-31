from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

# Create your models here.

class Series(models.Model):
    Match = models.CharField(max_length=264, unique=True)

    def __str__(self):
        return self.Match

    def get_absolute_url(self):
        return reverse("TeamPicker:CreatePlayer")

class Player(models.Model):
    Series = models.ForeignKey(Series, related_name = 'series',
                                on_delete=models.CASCADE)
    Name = models.CharField(max_length=264)
    Role = models.CharField(max_length=264, choices=[
                                            ('BAT', 'BAT'),
                                            ('BOWL', 'BOWL'),
                                            ('ALL', 'ALL'),
                                            ('WK', 'WK')
                                            ],
                            default="BAT"
    )
    Credit = models.FloatField()
    Team = models.CharField(max_length=264, choices=[
                                            ('Team1', 'Team1'),
                                            ('Team2','Team2')
                                            ],
                            default="Team1")
    def get_absolute_url(self):
        return reverse("TeamPicker:CreatePlayer")
