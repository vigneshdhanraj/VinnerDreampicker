from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, UpdateView, ListView, DetailView,
                                DeleteView)
from TeamPicker.forms import Player_List
from TeamPicker.models import Series, Player
import json
import glob
import os
import random

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SeriesCreateView(CreateView):
    model = Series
    fields = ('Match',)

class PlayerCreateView(CreateView):
    model = Player
    fields = ('Series', 'Name', 'Role', 'Credit', 'Team')

class SeriesListView(ListView):
    model = Series

class SeriesDetailView(DetailView):
    model = Series
    template_name = 'TeamPicker/series_detail.html'

class SeriesDeleteView(DeleteView):
    model = Series
    success_url = reverse_lazy("index")

class PlayerDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy("index")

class PlayerUpdateView(UpdateView):
    model = Player
    fields = ('Series', 'Name', 'Role', 'Credit', 'Team')

def combineteams(Teamlist):
    combineteam = []
    for team in Teamlist['Team']:
        if team.get("Team1"):
            for t in team['Team1']:
                t['Teamname'] = "Team1"
                combineteam.append(t)
        if team.get("Team2"):
            for t in team['Team2']:
                t['Teamname'] = "Team2"
                combineteam.append(t)
    return combineteam

def pickrandom(Teamlist):
    allrounder = 0
    bat = 0
    bowl = 0
    wk = 0
    team1 = 0
    team2 = 0
    teamlist = combineteams(Teamlist)
    sample = random.sample(teamlist, 11)
    for s in sample:
        if s['Teamname'] == "Team1":
            team1 = team1 + 1
        else:
            team2 = team2 + 1
        if s['Role'] == "ALL":
            allrounder = allrounder + 1
        elif s['Role'] == "BAT":
            bat = bat + 1
        elif s['Role'] == "BOWL":
            bowl = bowl + 1
        elif s['Role'] == "WK":
            wk = wk + 1
    total_credit = sum([float(s['Credit']) for s in sample])
    if (
        (
            (allrounder >= 1) and (
                allrounder <= 4)) and (
            (bat >= 3) and (
                bat <= 6)) and (
                    (bowl >= 3) and (
                        bowl <= 6)) and (
                            (wk >= 1) and (
                                wk <= 3))) and (
                                    (team1 >= 4) and (
                                        team1 <= 7)) and (
                                            total_credit <= 100.0):
        print("================================================================")
        print ("\nTotal Credit Used: " + str(total_credit) + "\n")
        print (
            "Bat: " +
            str(bat) +
            " Bowl: " +
            str(bowl) +
            " ALL: " +
            str(allrounder) +
            " WK: " +
            str(wk) +
            " Team1: " +
            str(team1) +
            " Team2: " +
            str(team2))

    else:
        total_credit = 0
        sample = pickrandom(Teamlist)

    print(sample)
    return sample

def selecting_cap(team):
    cap = random.sample(team, 2)
    captain = cap[0]['Name']
    vice_captain = cap[1]['Name']
    return {"CAPTAIN":captain, "VICE_CAPTAIN":vice_captain}

def run(request):
    Match = request.POST.getlist('id')[0]
    Team1_Players = list(Player.objects.filter(Series = Match).filter(Team="Team1").values())
    Team2_Players = list(Player.objects.filter(Series = Match).filter(Team="Team2").values())
    team_dict = {
        'Team1': Team1_Players,
        'Team2': Team2_Players
    }
    teams = {"Team":[team_dict]}
    team = pickrandom(teams)
    sorted_team = sorted(team, key=lambda i: i['Role'])
    total_credit = sum([float(s['Credit']) for s in sorted_team])
    wk = [s for s in sorted_team if s['Role'] == "WK"]
    bat = [s for s in sorted_team if s['Role'] == "BAT"]
    bowl = [s for s in sorted_team if s['Role'] == "BOWL"]
    allround = [s for s in sorted_team if s['Role'] == "ALL"]
    cap_vc = selecting_cap(sorted_team)
    data_dict = {"WK":wk, "BAT":bat, "BOWL":bowl, "ALL":allround,
                "CAPTAIN":cap_vc['CAPTAIN'],
                "VICE_CAPTAIN":cap_vc['VICE_CAPTAIN'],
                "id": Match, "CREDIT_USED":total_credit}
    return render(request, "TeamPicker/run.html", data_dict)
