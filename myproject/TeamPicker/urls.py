from django.urls import path
from TeamPicker import views

app_name = "TeamPicker"
urlpatterns = [
    path('run/', views.run, name="Run"),
    path('downloadteams/', views.downloadteams, name="DownloadTeams"),
    path('Create/', views.SeriesCreateView.as_view(), name="Create"),
    path('CreatePlayer/', views.PlayerCreateView.as_view(), name="CreatePlayer"),
    path('CreateTeam/', views.TeamCreateView.as_view(), name="CreateTeam"),
    path('TeamDetail/', views.TeamListView.as_view(), name="Team"),
    path('TeamDetail/<pk>/', views.TeamDetailView.as_view(), name="TeamDetail"),
    path('CreateTeamPlayer/', views.TeamPlayerCreateView.as_view(), name="CreateTeamPlayer"),
    path('Delete/<pk>', views.SeriesDeleteView.as_view(), name="Delete"),
    path('DeleteTeam/<pk>', views.TeamDeleteView.as_view(), name="DeleteTeam"),
    path('DeletePlayer/<pk>', views.PlayerDeleteView.as_view(), name="DeletePlayer"),
    path('DeleteTeamPlayer/<pk>', views.TeamPlayerDeleteView.as_view(), name="DeleteTeamPlayer"),
    path('UpdatePlayer/<pk>', views.PlayerUpdateView.as_view(), name="UpdatePlayer"),
    path('UpdateTeamPlayer/<pk>', views.TeamPlayerUpdateView.as_view(), name="UpdateTeamPlayer"),
]
