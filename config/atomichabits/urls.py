from django.urls import path

from atomichabits.apps import AtomichabitsConfig
from atomichabits.views import HabitListView, HabitDetailView, PublicHabitListView

app_name = AtomichabitsConfig.name

urlpatterns = [
    path('habits/', HabitListView.as_view(), name='habit_list_create'),
    path('habits/<int:pk>/', HabitDetailView.as_view(),
         name='habit_retrieve_update_destroy'),
    path('habits/public/', PublicHabitListView.as_view(),
         name='public_habits_list'),
]
