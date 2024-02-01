from django.urls import path
from .views import *

urlpatterns = [
    path('home_resto/', home_resto, name='home-resto'),
    path('home_facturation/', home_facturation, name='home-facturation'),
    # Routes concernant les Mp
    path('mp_list_pt/', mp_list_pt, name='mp-list-pt'),
    path('entree_mp_pt/', entree_mp_pt, name='entree-mp-pt'),
    path('delete_entree_mp_pt/<str:pk>/', delete_entree_pt, name='delete-entree-mp-pt'),
    path('sortie_mp_pt/', sortie_mp_pt, name='sortie-mp-pt'),
    path('delete_sortie_pt/<str:pk>/', delete_sortie_pt, name='delete-sortie-pt'),
    # Routes concernant les Pf
    path('pf_list_pt/', pf_pt_list, name='pf-pt-list'),
    path('cmd_pf/', cmd_pf, name='cmd-pf'),
    path('detail_cmd_pf/<str:pk>/', detail_cmd_pf, name='detail-cmd-pf'),
    path('delete_cmd_pf/<str:pk>/', delete_cmd_pf, name='delete-cmd-pf'),
    path('pf_detail_pt/<str:pk>/', pf_detail_pt, name='pf-detail-pt'),
    path('entree_pf_pt/', entree_pf_pt, name='entree-pf-pt'),
    path('delete_entree_pf_pt/<str:pk>/', delete_entree_pf_pt, name='delete-entree-pf-pt'),
    path('sortie_pf_pt/', sortie_pf_pt, name='sortie-pf-pt'),
    path('delete_sortie_pf_pt/<str:pk>/', delete_sortie_pf_pt, name='delete-sortie-pf-pt'),
    path('delete_pf_pt/<str:pk>/', delete_pf_pt, name='delete-pf-pt'),

    # Routes concernant la facturation
    path('facturation-resto/', add_cmd_pf, name='add-facturation'),
    path('change-qts/<str:pk>/', change_qts_pf, name='change-qts-pf'),
    path('delete-line-pf/<str:pk>/', delete_line_pf, name='delete-line-pf'),
    path('change-type-paiement/<str:pk>/', change_type_paiement, name='change-type-paiement'),
    path('detail-print-pf/<str:pk>/', detail_print_pf, name='detail-print-pf'),
    path('ventes-fact/', cmd_pf_facturation, name='cmd-pf-fact'),
    path('confirm-paiement/<str:pk>/', confirm_paiement, name='confirm-paiement'),
    path('detail_cmd_pf_fact/<str:pk>/', detail_cmd_pf_facturation, name='detail-cmd-pf-fact'),
    path('detail_cmd_pf_uncloture/<str:pk>/', detail_cmd_pf_uncloture, name='detail-cmd-pf-uncloture'),
    path('confirm_order/', confirm_order, name='confirm-order')

]
