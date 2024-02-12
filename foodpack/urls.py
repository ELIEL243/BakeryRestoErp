from django.urls import path
from .views import *

urlpatterns = [
    # Routes concernant les Mp
    path('mp_list_pack/', mp_list_pack, name='mp-list-pack'),
    path('entree_mp_pack/', entree_mp_pack, name='entree-mp-pack'),
    path('delete_entree_mp_pack/<str:pk>/', delete_entree_pack, name='delete-entree-mp-pack'),
    path('sortie_mp_pack/', sortie_mp_pack, name='sortie-mp-pack'),
    path('delete_sortie_pack/<str:pk>/', delete_sortie_pack, name='delete-sortie-pack'),

    # Concernant les packs

    path('home_foodpack/', home_foodpack, name='home-foodpack'),
    path('pack_list/', pack_list, name='pack-list'),
    path('pack_detail/<str:pk>/', pack_detail, name='pack-detail'),
    path('delete_pack/<str:pk>/', delete_pack, name='delete-pack'),
    path('entree_pack/', entree_pack, name='entree-pack'),
    path('delete_entree_pack/<str:pk>/', delete_entree_pack, name='delete-entree-pack'),
    path('sortie_pack/', sortie_pack, name='sortie-pack'),
    path('delete_sortie_pack/<str:pk>/', delete_sortie_pack, name='delete-sortie-pack'),
    path('invendu_pack/', invendu_pack, name='invendu-pack'),
    path('delete_invendu_pack/<str:pk>/', delete_invendu_pack, name='delete-invendu-pack'),
    path('entreprise_list/', entreprise_list, name='entreprise-list'),
    path('entreprise_detail/<str:pk>/', entreprise_detail, name='entreprise-detail'),
    path('delete_entreprise/<str:pk>/', delete_entreprise, name='delete-entreprise'),

]