from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('eqtl_result/', views.eqtl_search),
    path('gene_list/', views.show_gene_list),
    path('drug/', views.drug, name='drug'),
    path('drug_result/', views.drug_search)
]