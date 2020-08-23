from django.urls import path
from .views import (
    CarsListView,
    AddCarView,
    RepairsListView,
    UpdateCarView,
    DeleteCarView,
    AddRepairView
)
urlpatterns = [
    path('', CarsListView.as_view(), name='cars'),
    path('add-car/', AddCarView.as_view(), name='add_car'),
    path('car/', RepairsListView.as_view(), name='car_detail'),
    path('car/<int:pk>/update/', UpdateCarView.as_view(), name='update_car'),
    path('car/<int:pk>/delete/', DeleteCarView.as_view(), name='delete_car'),
    path('car/<int:pk>/new-repair/', AddRepairView.as_view(), name='add_repair'),
]
