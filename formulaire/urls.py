from django.urls import path
from .import views

urlpatterns = [
    path('',views.getFormulaire, name='formulaire_view'),
    
]
