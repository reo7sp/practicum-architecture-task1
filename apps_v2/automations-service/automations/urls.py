from django.urls import path
from .views import CreateScenarioView, ListScenariosView, ScenarioDetailView

urlpatterns = [
    path('scenarios/', CreateScenarioView.as_view(), name='create_scenario'),
    path('scenarios/', ListScenariosView.as_view(), name='list_scenarios'),
    path('scenarios/<uuid:id>', ScenarioDetailView.as_view(), name='scenario_detail'),
]
