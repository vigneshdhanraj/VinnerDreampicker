from django.urls import path
from TeamPicker import views

app_name = "TeamPicker"
urlpatterns = [
    path('run/', views.run, name="Run"),
    path('Create/', views.SeriesCreateView.as_view(), name="Create"),
    path('CreatePlayer/', views.PlayerCreateView.as_view(), name="CreatePlayer"),
    path('Delete/<pk>', views.SeriesDeleteView.as_view(), name="Delete"),
    path('DeletePlayer/<pk>', views.PlayerDeleteView.as_view(), name="DeletePlayer"),
    path('UpdatePlayer/<pk>', views.PlayerUpdateView.as_view(), name="UpdatePlayer"),
]
