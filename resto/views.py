from django.shortcuts import render, redirect
import datetime
import calendar
import decimal
from pathlib import Path
from time import strftime
from django.db.models import Q, Sum, Count, F, Avg
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.http import HttpResponse

from bakery.models import *
from resto.models import *
from django.contrib.auth.decorators import login_required
import uuid
from auth_user.decorators import allowed_users


# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def home_resto(request):
    return render(request, 'resto/home_resto.html', context={})


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def home_facturation(request):
    return render(request, 'resto/home_facturation.html', context={})


# Vues concernant les matieres premieres
# Vues concernant les matieres premieres
# Vues concernant les matieres premieres
@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def mp_list_pt(request):
    mps = MatierePremiere.objects.filter(type_mp__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])

    return render(request, 'resto/mp_list.html', context={'mps': mps})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def entree_mp_pt(request):
    mps = MatierePremiere.objects.filter(type_mp__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])
    entries = EntreeMpPt.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            EntreeMpPt.objects.create(matiere_premiere=mp, qts=qts)
            messages.success(request, 'good !')
            return redirect('entree-mp-pt')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreeMpPt.objects.filter(date=date1)
        else:
            entries = EntreeMpPt.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'resto/entree_mp.html',
                  context={'mps': mps, 'entries': entries, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def sortie_mp_pt(request):
    mps = MatierePremiere.objects.filter(type_mp__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])
    outs = SortieMpPt.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if mp.in_stock_pt >= qts:
                SortieMpPt.objects.create(matiere_premiere=mp, qts=qts)
                messages.success(request, 'good !')
                return redirect('sortie-mp-pt')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-mp-pt')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortieMpPt.objects.filter(date=date1)
        else:
            outs = SortieMpPt.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'resto/sortie_mp.html', context={'mps': mps, 'outs': outs, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def delete_entree_pt(request, pk):
    EntreeMpPt.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-mp-pt')


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def delete_sortie_pt(request, pk):
    SortieMpPt.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-mp-pt')


# Vues concernant les produits finis
# Vues concernant les produits finis
# Vues concernant les produits finis

@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def pf_pt_list(request):
    pfs = ProduitFini.objects.filter(type_produit__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])
    units = Unite.objects.all()
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            unit_name = request.POST.get('unit')
            critic_qts = int(request.POST.get('qts'))
            price = int(request.POST.get('price'))
            unit = Unite.objects.get(name=unit_name)
            type_prod = 'RESTAURANT'
            ProduitFini.objects.create(libelle=name, description=desc, price=price, unite=unit, critic_qts=critic_qts,
                                       type_produit=type_prod)
            messages.success(request, 'good !')
            return redirect('pf-pt-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'resto/pf_list.html', context={'pfs': pfs, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def entree_pf_pt(request):
    pfs = ProduitFini.objects.filter(type_produit__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])
    entries = EntreePfPt.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).exists():
            pf = ProduitFini.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            EntreePfPt.objects.create(produit_fini=pf, qts=qts)
            messages.success(request, 'good !')
            return redirect('entree-pf-pt')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreePfPt.objects.filter(date=date1)
        else:
            entries = EntreePfPt.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'resto/entree_pf.html',
                  context={'pfs': pfs, 'entries': entries, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def sortie_pf_pt(request):
    pfs = ProduitFini.objects.filter(type_produit__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])
    outs = SortiePfPt.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).exists():
            pf = ProduitFini.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if pf.in_stock >= qts:
                SortiePfPt.objects.create(produit_fini=pf, qts=qts, price=pf.price)
                messages.success(request, 'good !')
                return redirect('sortie-pf-pt')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-pf-pt')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortiePfPt.objects.filter(date=date1)
        else:
            outs = SortiePfPt.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'resto/sortie_pf.html', context={'pfs': pfs, 'outs': outs, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def delete_entree_pf_pt(request, pk):
    EntreePfPt.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-pf-pt')


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def delete_sortie_pf_pt(request, pk):
    SortiePfPt.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-pf-pt')


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def delete_pf_pt(request, pk):
    pf = ProduitFini.objects.get(pk=pk)
    pf.delete()
    messages.success(request, 'good !')
    return redirect('pf-pt-list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def pf_detail_pt(request, pk):
    units = Unite.objects.all()
    pf = ProduitFini.objects.get(pk=pk)
    if request.method == 'POST':
        if ProduitFini.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            pf.libelle = request.POST.get('name')
            pf.description = request.POST.get('desc')
            pf.critic_qts = int(request.POST.get('qts'))
            pf.price = int(request.POST.get('price'))
            pf.unit = Unite.objects.get(name=request.POST.get('unit'))
            pf.save()
            messages.success(request, 'good !')
            return redirect('pf-pt-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'resto/forms/pf_detail.html', context={'pf': pf, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def cmd_pf(request):
    orders = CommandePf.objects.all().order_by('-date')
    ord1 = orders.filter(devise__isnull=True)
    for i in ord1:
        i.delete()
    ref = generate_unique_uid()
    date1 = None
    date2 = None
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            orders = orders.filter(date=date1)
        else:
            orders = orders.filter(Q(date__gte=date1) & Q(date__lte=date2))

    return render(request, 'resto/ventes.html', context={'orders': orders, 'ref': ref, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['petit stock restaurant'])
def detail_cmd_pf(request, pk):
    order = CommandePf.objects.get(pk=pk)
    lines = LigneCommandePf.objects.filter(commande=order)

    return render(request, 'resto/forms/detail_cmd_pf.html', context={'lines': lines, 'order': order})


@login_required(login_url='login')
#@allowed_users(allowed_roles=['petit stock restaurant', 'caisse restaurant'])
def delete_cmd_pf(request, pk):
    order = CommandePf.objects.get(pk=pk)
    order.delete()
    messages.success(request, 'good !')
    return redirect('cmd-pf')


# Vues concernant la facturation

@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def add_cmd_pf(request):
    order, created = CommandePf.objects.get_or_create(etat=False)
    table = None
    if created:
        order.ref = generate_unique_uid()

    lines = LigneCommandePf.objects.filter(commande=order)
    pfs = ProduitFini.objects.filter(type_produit__in=['BOULANGERIE ET RESTAURANT', 'RESTAURANT'])
    if request.method == 'POST':
        if request.POST.get('add') is not None:
            name = request.POST.get('name')
            client_name = request.POST.get('client')
            order.client = client_name
            table = int(request.POST.get('table'))
            order.table_number = table
            order.devise = "FC"
            order.save()
            qts = request.POST.get('qts')
            if ProduitFini.objects.filter(libelle=name).count() > 0:
                pf = ProduitFini.objects.get(libelle=name)
                line, created = LigneCommandePf.objects.get_or_create(commande=order, produit_fini=pf)
                line.qts += int(qts)
                line.price = pf.price

                line.save()
                messages.success(request, "Succes")
            else:
                messages.error(request, "Echec")
        elif request.POST.get('confirm') is not None:
            type_p = request.POST.get('type')
            if type_p == "A crédit":
                order.paid = False
                order.client = request.POST.get('client')
            else:
                order.paid = True
            order.etat = True
            order.save()
            return redirect('detail-print-pf', pk=order.pk)

    return render(request, 'resto/add_facturation.html',
                  context={'order': order, 'pfs': pfs, 'lines': lines, 'table': table})


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def change_qts_pf(request, pk):
    line = LigneCommandePf.objects.get(pk=pk)
    if request.GET.get('qts') is not None:
        line.qts = int(request.GET.get('qts'))
    elif request.GET.get('qts') is None:
        line.qts = 1
    line.save()
    order = line.commande
    lines = LigneCommandePf.objects.filter(commande=order)
    return render(request, 'resto/partials/update_facturation.html', context={'order': order, 'lines': lines})


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def delete_line_pf(request, pk):
    LigneCommandePf.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('add-facturation')


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def change_type_paiement(request, pk):
    order = CommandePf.objects.get(pk=pk)
    type_p = request.GET.get('type')
    if type_p == "A crédit":
        order.paid = False
    else:
        order.paid = True

    return render(request, 'resto/partials/client_pf.html', context={'is_credit': order.paid})


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def detail_print_pf(request, pk):
    order = CommandePf.objects.get(pk=pk)
    lines = LigneCommandePf.objects.filter(commande=order)

    return render(request, 'resto/forms/detail-print2.html', context={'lines': lines, 'order': order})


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def cmd_pf_facturation(request):
    orders = CommandePf.objects.all().order_by('date')
    ord1 = orders.filter(devise__isnull=True)
    for i in ord1:
        i.delete()
    ref = generate_unique_uid()
    date1 = None
    date2 = None
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            orders = orders.filter(date=date1)
        else:
            orders = orders.filter(Q(date__gte=date1) & Q(date__lte=date2))

    return render(request, 'resto/ventes_facturation.html',
                  context={'orders': orders, 'ref': ref, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def confirm_paiement(request, pk):
    order = CommandePf.objects.get(pk=pk)
    order.paid = True
    order.save()
    return redirect('cmd-pf-fact')


@login_required(login_url='login')
@allowed_users(allowed_roles=['caisse restaurant'])
def detail_cmd_pf_facturation(request, pk):
    order = CommandePf.objects.get(pk=pk)
    lines = LigneCommandePf.objects.filter(commande=order)

    return render(request, 'resto/forms/detail_cmd_pf_fact.html', context={'lines': lines, 'order': order})


def confirm_order(request):
    messages.success(request, "good !")
    return redirect('add-facturation')