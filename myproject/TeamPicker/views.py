from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView, UpdateView, ListView, DetailView,
                                DeleteView)
from TeamPicker.forms import Player_List
from TeamPicker.models import Series, Player, Team, TeamPlayer
import json
import glob
import os
import random

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SeriesCreateView(CreateView):
    model = Series
    fields = ('Match','WinningChance')

class TeamCreateView(CreateView):
    model = Team
    fields = ('Team',)

class TeamListView(ListView):
    model = Team

class TeamDetailView(DetailView):
    model = Team
    template_name = 'TeamPicker/team_detail.html'

class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy("index")

class TeamPlayerCreateView(CreateView):
    model = TeamPlayer
    fields = ('Team', 'Name', 'Role', 'Credit')

class TeamPlayerUpdateView(UpdateView):
    model = TeamPlayer
    fields = ('Team', 'Name', 'Role', 'Credit')

class TeamPlayerDeleteView(DeleteView):
    model = TeamPlayer
    success_url = reverse_lazy("TeamPicker:Team")

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
        # print("================================================================")
        # print ("\nTotal Credit Used: " + str(total_credit) + "\n")
        # print (
        #     "Bat: " +
        #     str(bat) +
        #     " Bowl: " +
        #     str(bowl) +
        #     " ALL: " +
        #     str(allrounder) +
        #     " WK: " +
        #     str(wk) +
        #     " Team1: " +
        #     str(team1) +
        #     " Team2: " +
        #     str(team2))
        pass

    else:
        total_credit = 0
        sample = pickrandom(Teamlist)

    # print(sample)
    return sample

def selecting_cap(team):
    cap = random.sample(team, 2)
    captain = cap[0]['Name']
    vice_captain = cap[1]['Name']
    return {"CAPTAIN":captain, "VICE_CAPTAIN":vice_captain}

def getTeamDict(teamname):
    teams = list(Team.objects.filter(Team = teamname).values())
    team_dict = teams[0]
    return team_dict

def getMatchDict(matchname):
    match = list(Series.objects.filter(Match = matchname).values())
    match_dict = match[0]
    return match_dict

def downloadteams(request):
    match = request.POST.getlist('Match')[0]
    match_ins = Series.objects.create(Match = match)
    match_id = getMatchDict(match)
    match_teams = match.split('VS')
    team1 = match_teams[0]
    team2 = match_teams[1]
    team1_id = getTeamDict(team1)['id']
    team2_id = getTeamDict(team2)['id']
    Team1_Players = list(TeamPlayer.objects.filter(Team = team1_id).values())
    Team2_Players = list(TeamPlayer.objects.filter(Team = team2_id).values())
    if Team1_Players:
        for Team in Team1_Players:
            Player.objects.create(Series = match_ins, Name = Team['Name'], Role = Team['Role'], Credit = Team['Credit'], Team = "Team1")
    if Team2_Players:
        for Team in Team2_Players:
            Player.objects.create(Series = match_ins, Name = Team['Name'], Role = Team['Role'], Credit = Team['Credit'], Team = "Team2")
    return HttpResponseRedirect("/")


def run_team(teams, match):
    team = pickrandom(teams)
    sorted_team = sorted(team, key=lambda i: i['Role'])
    count = 0
    for s in sorted_team:
        if s['Team'] == "Team1":
            count = count + 1
    total_credit = sum([float(s['Credit']) for s in sorted_team])
    wk = [s for s in sorted_team if s['Role'] == "WK"]
    bat = [s for s in sorted_team if s['Role'] == "BAT"]
    bowl = [s for s in sorted_team if s['Role'] == "BOWL"]
    allround = [s for s in sorted_team if s['Role'] == "ALL"]
    cap_vc = selecting_cap(sorted_team)
    data_dict = {"WK":wk, "BAT":bat, "BOWL":bowl, "ALL":allround,
                "CAPTAIN":cap_vc['CAPTAIN'],
                "VICE_CAPTAIN":cap_vc['VICE_CAPTAIN'],
                "id": match, "CREDIT_USED":total_credit}
    return data_dict, count

def writejson(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    return 0


def readjson(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

def reset(request):
    jsonpath =  BASE_DIR + "/series_json/*"
    files = glob.glob(jsonpath)
    for f in files:
        os.remove(f)
    return HttpResponseRedirect("/")

def create_data_dict(teams, Match, Team_support):
    data_dict, count = run_team(teams, Match)
    if Team_support:
        if Team_support[0] == "Team1":
            while(count != 7):
                data_dict, count = run_team(teams, Match)
        else:
            while(count != 4 ):
                data_dict, count = run_team(teams, Match)
    return data_dict

def assign_teams(data_dict, team1, team2):
    for i in data_dict['WK']:
        if i['Team'] == "Team1":
            i['Team'] = team1
        else:
            i['Team'] = team2
    for i in data_dict['BOWL']:
        if i['Team'] == "Team1":
            i['Team'] = team1
        else:
            i['Team'] = team2
    for i in data_dict['BAT']:
        if i['Team'] == "Team1":
            i['Team'] = team1
        else:
            i['Team'] = team2
    for i in data_dict['ALL']:
        if i['Team'] == "Team1":
            i['Team'] = team1
        else:
            i['Team'] = team2
    return data_dict

def run(request):
    data_list = []
    Match = request.POST.getlist('id')[0]
    Team_support = request.POST.getlist('team')
    match_detail = list(Series.objects.filter(id = Match).values())
    team1 = match_detail[0]['Match'].split("VS")[0]
    team2 = match_detail[0]['Match'].split("VS")[1]
    # series_id = list(Player.objects.filter(Series = Match).values())[0]['Series_id']
    # jsonpath =  BASE_DIR + "/series_json/" + str(series_id) + ".json"
    # if os.path.exists(jsonpath):
    #     data = readjson(jsonpath)
    #     if len(data) == 0:
    #         os.remove(jsonpath)
    #     else:
    #         for d in data:
    #             ren = render(request, "TeamPicker/run.html", d)
    #             data.remove(d)
    #             writejson(jsonpath, data)
    #             return ren
    # WinningChance = list(Series.objects.filter(id = series_id).values())[0]['WinningChance']
    Team1_Players = list(Player.objects.filter(Series = Match).filter(Team="Team1").values())
    Team2_Players = list(Player.objects.filter(Series = Match).filter(Team="Team2").values())
    team_dict = {
        'Team1': Team1_Players,
        'Team2': Team2_Players
    }
    teams = {"Team":[team_dict]}
    data_dict = create_data_dict(teams, Match, Team_support)
    data_dict = assign_teams(data_dict, team1, team2)

    # for i in range(10):
    #     data = run_team(teams, Match)
    #     data_list.append(data)
    # writejson(jsonpath, data_list)
    return render(request, "TeamPicker/run.html", data_dict)
