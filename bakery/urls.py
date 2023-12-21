from django.urls import path
from .views import *
urlpatterns = [
    # Rootes des unités
    path('home_bakery/', home_bakery, name='home-bakery'),
    path('unit_list/', unit_list, name='unit-list'),
    path('unit_detail/<str:pk>/', unit_detail, name='unit-detail'),
    path('delete_unit/<str:pk>/', delete_unit, name='delete-unit'),

    # Routes matières premières

    path('mp_list/', mp_list, name='mp-list'),
    path('mp_detail/<str:pk>/', mp_detail, name='mp-detail'),
    path('delete_mp/<str:pk>/', delete_mp, name='delete-mp'),
    path('entree_mp/', entree_mp, name='entree-mp'),
    path('edit_entree_mp/<str:pk>/', edit_entree_mp, name='edit-entree-mp'),
    path('delete_entree_mp/<str:pk>/', delete_entree, name='delete-entree-mp'),
    path('sortie_mp/', sortie_mp, name='sortie-mp'),
    path('delete_sortie/<str:pk>/', delete_sortie, name='delete-sortie'),
    path('cmd_mp/', cmd_mp, name='cmd-mp'),
    path('detail_cmd_mp/<str:ref>/', detail_cmd_mp, name='detail-cmd-mp'),
    path('add_cmd_mp/<str:ref>/', add_cmd_mp, name='add-cmd-mp'),
    path('delete_cmd_mp/<str:pk>/', delete_cmd, name='delete-cmd-mp'),
    path('confirm_cmd_mp/<str:ref>/', confirm_cmd_mp, name='confirm-cmd-mp'),
    path('edit_line_cmd_mp/<str:pk>/', edit_line_cmd_mp, name='edit-line-cmd-mp'),
    path('delete_line_cmd_mp/<str:pk>/', delete_line_cmd_mp, name='delete-line-cmd-mp'),

    # Routes des produits finis
    path('pf_list/', pf_list, name='pf-list'),
    path('pf_detail/<str:pk>/', pf_detail, name='pf-detail'),
    path('delete_pf/<str:pk>/', delete_pf, name='delete-pf'),
    path('entree_pf/', entree_pf, name='entree-pf'),
    #path('edit_entree_pf/<str:pk>/', edit_entree_pf, name='edit-entree-pf'),
    path('delete_entree_pf/<str:pk>/', delete_entree_pf, name='delete-entree-pf'),
    path('sortie_pf/', sortie_pf, name='sortie-pf'),
    path('delete_sortie_pf/<str:pk>/', delete_sortie_pf, name='delete-sortie-pf'),

    # Routes des fournitures

    path('fourniture_list/', fourniture_list, name='fourniture-list'),
    path('fourniture_detail/<str:pk>/', fourniture_detail, name='fourniture-detail'),
    path('delete_fourniture/<str:pk>/', delete_fourniture, name='delete-fourniture'),
    path('entree_fourniture/', entree_fourniture, name='entree-fourniture'),
    #path('edit_entree_mp/<str:pk>/', edit_entree_mp, name='edit-entree-mp'),
    path('delete_entree_fourniture/<str:pk>/', delete_entree_fourniture, name='delete-entree-fourniture'),
    path('sortie_fourniture/', sortie_fourniture, name='sortie-fourniture'),
    path('delete_sortie_fourniture/<str:pk>/', delete_sortie_fourniture, name='delete-sortie-fourniture'),
    path('cmd_fourniture/', cmd_fourniture, name='cmd-fourniture'),
    path('detail_cmd_fourniture/<str:ref>/', detail_cmd_fourniture, name='detail-cmd-fourniture'),
    path('add_cmd_fourniture/<str:ref>/', add_cmd_fourniture, name='add-cmd-fourniture'),
    path('delete_cmd_fourniture/<str:pk>/', delete_cmd_fourniture, name='delete-cmd-fourniture'),
    path('confirm_cmd_fourniture/<str:ref>/', confirm_cmd_fourniture, name='confirm-cmd-fourniture'),
    path('edit_line_cmd_fourniture/<str:pk>/', edit_line_cmd_fourniture, name='edit-line-cmd-fourniture'),
    path('delete_line_cmd_fourniture/<str:pk>/', delete_line_cmd_fourniture, name='delete-line-cmd-fourniture'),

    # Routes des fournisseurs

    path('fournisseur_list/', fournisseur_list, name='fournisseur-list'),
    path('fournisseur_detail/<str:pk>/', fournisseur_detail, name='fournisseur-detail'),
    path('delete_fournisseur/<str:pk>/', delete_fournisseur, name='delete-fournisseur'),

    # Routes des alertes

    path('check_critics/', check_critics, name='check-critics'),
    path('stop_critics/', stop_critics, name='stop-critics'),


]