import datetime
import calendar
import decimal
from pathlib import Path
from time import strftime

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .utils import get_day_name, get_month_name
from django.db.models import Q, Sum, Count, F, Avg
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractYear
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid
from auth_user.decorators import allowed_users

# Create your views here.


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


def current_taux():
    taux = 1
    if Taux.objects.all().count() > 0:
        taux = Taux.objects.all().last().valeur
    return taux


# Vues Concernant le dashboard
# Vues Concernant le dashboard
# Vues Concernant le dashboard
# Vues Concernant le dashboard

@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def main_dashboard(request):
    chiffre_affaire = 0
    outs = SortiePF.objects.filter(date=datetime.datetime.today().date())
    chf_a = ChiffreAffaire.objects.filter(date=datetime.datetime.today().date())
    cmd_cours = CommandeMp.objects.filter(etat=False).count() + CommandeFourniture.objects.filter(etat=False).count()
    cmd_liv = CommandeMp.objects.filter(etat=True,
                                        delivered_at=datetime.datetime.today().date()).count() + CommandeFourniture.objects.filter(
        etat=True, delivered_at=datetime.datetime.today().date()).count()
    stock_critics = 0

    for i in MatierePremiere.objects.all():
        if i.in_stock <= i.critic_qts:
            stock_critics += 1
    for i in ProduitFini.objects.all():
        if i.in_stock <= i.critic_qts:
            stock_critics += 1
    for i in Fourniture.objects.all():
        if i.in_stock <= i.critic_qts:
            stock_critics += 1
    if len(chf_a) > 0:
        chiffre_affaire = chf_a.last().total_price
    elif len(chf_a) == 0:
        for out in outs:
            chiffre_affaire += out.total_cost
    return render(request, 'bakery/main_dashboard.html',
                  context={'chiffre_affaires': chiffre_affaire, 'cmd_cours': cmd_cours, 'cmd_liv': cmd_liv,
                           'stock_critics': stock_critics})


# Stats en rapport avec les matières premières
@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def stat_mp(request):
    default_date = datetime.datetime.today()
    date1 = default_date.date()
    date2 = date1 + datetime.timedelta(days=30)
    first_day = datetime.date(date1.year, 1, 1).strftime("%Y-%m-%d")
    date1.strftime("%Y-%m-%d")
    date2.strftime("%Y-%m-%d")
    actual_year = default_date.year
    actual_month = default_date.month
    actual_day = default_date.day
    years = [i for i in range(2020, 2100)]
    months = [i for i in range(1, 13)]
    days = [i for i in range(1, 31)]
    entries = EntreeMp.objects.filter(date__year=default_date.year, date__month=default_date.month)
    for i in entries:
        if i.devise == "USD":
            i.price = i.price * i.taux
    entries = entries.annotate(day=ExtractDay('date')).values('day').annotate(total=Sum('price')).order_by('day')
    for i in entries:
        i["day"] = f'{i["day"]} {get_month_name(default_date.month)}'
    nbr_cmd = LigneCommandeMp.objects.filter(commande__date__year=default_date.year)
    for i in nbr_cmd:
        if i.devise == "USD":
            i.total_price = i.total_price * i.taux
    nbr_cmd = nbr_cmd.values('matiere_premiere__libelle').annotate(total=Count('commande__id'),
                                                                   total_price=Sum('total_price'))
    print(nbr_cmd)
    mps = MatierePremiere.objects.all()
    return render(request, 'bakery/stat_mp.html',
                  context={'actual_year': actual_year, 'actual_month': actual_month, 'actual_day': actual_day,
                           'total_cost': entries, 'nbr_cmd': nbr_cmd, 'mps': mps, 'years': years, 'months': months,
                           'date1': str(date1), 'date2': date2, 'first_day': first_day})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_cost_mp(request):
    default_date = datetime.datetime.today()
    year = request.GET.get('year')
    month = request.GET.get('month')
    is_year_only = False
    entries = None
    if month is None or month == "Aucun":
        entries = EntreeMp.objects.filter(date__year=year)
        for i in entries:
            if i.devise == "USD":
                i.price = i.price * i.taux

        entries = entries.annotate(month=ExtractMonth('date')).values('month').annotate(total=Sum('price')).order_by(
            'month')
        for entry in entries:
            month_number = entry['month']
            month_name = get_month_name(month_number)
            entry['month'] = month_name
        is_year_only = True
    else:
        entries = EntreeMp.objects.filter(date__year=year, date__month=month)
        for i in entries:
            if i.devise == "USD":
                i.price = i.price * i.taux

        entries = entries.annotate(day=ExtractDay('date')).values('day').annotate(total=Sum('price')).order_by('day')
        for i in entries:
            i["day"] = f'{i["day"]} {get_month_name(int(month))}'

    return render(request, 'bakery/partials/cost_mp.html',
                  context={'total_cost': entries, 'is_year_only': is_year_only})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_cmd_mp(request):
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    nbr_cmd = None
    if date2 == "" or date2 is None:
        nbr_cmd = LigneCommandeMp.objects.filter(commande__date=date1)
        for i in nbr_cmd:
            if i.devise == "USD":
                i.total_price = i.total_price * i.taux
        nbr_cmd = nbr_cmd.values(
            'matiere_premiere__libelle').annotate(total=Count('commande__id'), total_price=Sum('total_price'))
    else:
        nbr_cmd = LigneCommandeMp.objects.filter(Q(commande__date__gte=date1) & Q(commande__date__lte=date2))
        for i in nbr_cmd:
            if i.devise == "USD":
                i.total_price = i.total_price * i.taux
        nbr_cmd = nbr_cmd.values(
            'matiere_premiere__libelle').annotate(total=Count('commande__id'), total_price=Sum('total_price'))

    return render(request, 'bakery/partials/nbr_cmd_mp.html', context={'nbr_cmd': nbr_cmd})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_entry_out_mp(request):
    mps = MatierePremiere.objects.all()
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    for i in mps:
        i.total_out = i.qts_out_by_date(date1, date2)
        i.total_entry = i.qts_enter_by_date(date1, date2)
    for i in mps:
        print(i.total_out)
        print(i.total_entry)
    return render(request, 'bakery/partials/nbr_entry_out_mp.html', context={'mps': mps})


# Stat en rapport avec les fourniture
@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def stat_fourniture(request):
    default_date = datetime.datetime.today()
    date1 = default_date.date()
    date2 = date1 + datetime.timedelta(days=30)
    first_day = datetime.date(date1.year, 1, 1).strftime("%Y-%m-%d")
    date1.strftime("%Y-%m-%d")
    date2.strftime("%Y-%m-%d")
    actual_year = default_date.year
    actual_month = default_date.month
    actual_day = default_date.day
    years = [i for i in range(2020, 2100)]
    months = [i for i in range(1, 13)]
    entries = EntreeFourniture.objects.filter(date__year=default_date.year, date__month=default_date.month)
    for i in entries:
        if i.devise == "USD":
            i.price = i.price * i.taux
    entries = entries.annotate(day=ExtractDay('date')).values('day').annotate(total=Sum('price')).order_by('day')
    for i in entries:
        i["day"] = f'{i["day"]} {get_month_name(default_date.month)}'
    nbr_cmd = LigneCommandeFourniture.objects.filter(commande__date__year=default_date.year)
    for i in nbr_cmd:
        if i.devise == "USD":
            i.total_price = i.total_price * i.taux
    nbr_cmd = nbr_cmd.values('fourniture__libelle').annotate(total=Count('commande__id'),
                                                             total_price=Sum('total_price'))

    fournitures = Fourniture.objects.all()

    return render(request, 'bakery/stat-fourniture.html',
                  context={'actual_year': actual_year, 'actual_month': actual_month, 'actual_day': actual_day,
                           'total_cost': entries, 'nbr_cmd': nbr_cmd, 'fournitures': fournitures, 'years': years,
                           'months': months, 'date1': str(date1), 'date2': date2, 'first_day': first_day})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_cost_fourniture(request):
    default_date = datetime.datetime.today()
    year = request.GET.get('year')
    month = request.GET.get('month')
    is_year_only = False
    entries = None
    if month is None or month == "Aucun":
        entries = EntreeFourniture.objects.filter(date__year=year)
        for i in entries:
            if i.devise == "USD":
                i.price = i.price * i.taux

        entries = entries.annotate(month=ExtractMonth('date')).values('month').annotate(total=Sum('price')).order_by(
            'month')
        for entry in entries:
            month_number = entry['month']
            month_name = get_month_name(month_number)
            entry['month'] = month_name
        is_year_only = True
    else:
        entries = EntreeFourniture.objects.filter(date__year=year, date__month=month)
        for i in entries:
            if i.devise == "USD":
                i.price = i.price * i.taux

        entries = entries.annotate(day=ExtractDay('date')).values('day').annotate(total=Sum('price')).order_by('day')
        for i in entries:
            i["day"] = f'{i["day"]} {get_month_name(int(month))}'

    return render(request, 'bakery/partials/cost_fourniture.html',
                  context={'total_cost': entries, 'is_year_only': is_year_only})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_cmd_fourniture(request):
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    nbr_cmd = None
    if date2 == "" or date2 is None:
        nbr_cmd = LigneCommandeFourniture.objects.filter(commande__date=date1)
        for i in nbr_cmd:
            if i.devise == "USD":
                i.total_price = i.total_price * i.taux
        nbr_cmd = nbr_cmd.values(
            'fourniture__libelle').annotate(total=Count('commande__id'), total_price=Sum('total_price'))
    else:
        nbr_cmd = LigneCommandeFourniture.objects.filter(Q(commande__date__gte=date1) & Q(commande__date__lte=date2))
        for i in nbr_cmd:
            if i.devise == "USD":
                i.total_price = i.total_price * i.taux
        nbr_cmd = nbr_cmd.values(
            'fourniture__libelle').annotate(total=Count('commande__id'), total_price=Sum('total_price'))

    return render(request, 'bakery/partials/nbr_cmd_fourniture.html', context={'nbr_cmd': nbr_cmd})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_entry_out_fourniture(request):
    fournitures = Fourniture.objects.all()
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    for i in fournitures:
        i.total_out = i.qts_out_by_date(date1, date2)
        i.total_entry = i.qts_enter_by_date(date1, date2)
    return render(request, 'bakery/partials/nbr_entry_out_fourniture.html', context={'fournitures': fournitures})


# En rapport avec les produits finis
@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def stat_pf(request):
    default_date = datetime.datetime.today()
    date1 = default_date.date()
    date2 = date1 + datetime.timedelta(days=30)
    first_day = datetime.date(date1.year, 1, 1).strftime("%Y-%m-%d")
    last_day = datetime.date(date1.year, 12, 31).strftime("%Y-%m-%d")
    date1.strftime("%Y-%m-%d")
    date2.strftime("%Y-%m-%d")
    actual_year = default_date.year
    actual_month = default_date.month
    actual_day = default_date.day
    years = [i for i in range(2020, 2100)]
    months = [i for i in range(1, 13)]
    cmds = CommandePf.objects.filter(date__year=default_date.year, date__month=default_date.month)
    for i in cmds:
        i.temp_total = int(i.get_total)
    entries = cmds.annotate(day=ExtractDay('date')).values(
        'day').annotate(total_price=Sum(1)).order_by('day')
    for i in entries:
        i["day"] = f'{i["day"]} {get_month_name(int(default_date.month))}'
        print(i["total_price"])
    pfs = ProduitFini.objects.all()
    for i in pfs:
        i.total_sale = int(i.total_sale_by_date(first_day, last_day))

    return render(request, 'bakery/stat_pf.html',
                  context={'actual_year': actual_year, 'actual_month': actual_month, 'actual_day': actual_day,
                           'total_cost': entries, 'pfs': pfs, 'years': years, 'months': months, 'date1': str(date1),
                           'date2': date2, 'first_day': first_day})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_chf_pf(request):
    default_date = datetime.datetime.today()
    year = request.GET.get('year')
    month = request.GET.get('month')
    is_year_only = False
    entries = None
    cmds = CommandePf.objects.filter(date__year=year)
    for i in cmds:
        i.temp_total = i.get_total
    if month is None or month == "Aucun":
        entries = cmds.filter(date__year=year).annotate(month=ExtractMonth('date')).values(
            'month').annotate(total_price=Sum('temp_total')).order_by('month')
        for entry in entries:
            month_number = entry['month']
            month_name = get_month_name(month_number)
            entry['month'] = month_name
        is_year_only = True
    else:
        entries = cmds.filter(date__year=year, date__month=month).annotate(day=ExtractDay('date')).values('day').annotate(total_price=Sum('temp_total')).order_by('day')
        for i in entries:
            i["day"] = f'{i["day"]} {get_month_name(int(month))}'
    return render(request, 'bakery/partials/chf_pf.html', context={'total_cost': entries, 'is_year_only': is_year_only})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_sale_pf(request):
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    pfs = ProduitFini.objects.all()
    if date2 == "" or date2 is None:
        for i in pfs:
            i.total_sale = int(i.total_sale_by_date_pt(date1, date2))
    else:
        for i in pfs:
            i.total_sale = int(i.total_sale_by_date_pt(date1, date2))
    return render(request, 'bakery/partials/total_sale_pf.html', context={'pfs': pfs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_entry_out_pf(request):
    pfs = ProduitFini.objects.all()
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    for i in pfs:
        i.total_out = i.qts_out_by_date(date1, date2)
        i.total_entry = i.qts_enter_by_date(date1, date2)
    return render(request, 'bakery/partials/nbr_entry_out_pf.html', context={'pfs': pfs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def filter_total_entry_out_pf_pt(request):
    pfs = ProduitFini.objects.all()
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    for i in pfs:
        i.total_out = i.qts_out_by_date_pt(date1, date2)
        i.total_entry = i.qts_enter_by_date_pt(date1, date2)
    return render(request, 'bakery/partials/nbr_entry_out_pf.html', context={'pfs': pfs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def home_bakery(request):
    chf_aff = ChiffreAffaire.objects.get_or_create(date=datetime.datetime.today().date())
    return render(request, 'bakery/home_bakery.html', context={})


# Vues concernant les unités
# Vues concernant les unités
# Vues concernant les unités
@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def unit_list(request):
    units = Unite.objects.all()
    if request.method == 'POST':
        if Unite.objects.filter(name=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            Unite.objects.create(name=name)
            messages.success(request, 'good !')
            return redirect('unit-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/unit_list.html', context={'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def unit_detail(request, pk):
    unit = Unite.objects.get(pk=pk)
    if request.method == 'POST':
        if Unite.objects.exclude(pk=pk).filter(name=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            unit.name = name
            unit.save()
            messages.success(request, 'good !')
            return redirect('unit-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/unit_detail_form.html', context={'unit': unit})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_unit(request, pk):
    unit = Unite.objects.get(pk=pk)
    unit.delete()
    messages.success(request, 'good !')
    return redirect('unit-list')


# Vues concernant les matieres premieres
# Vues concernant les matieres premieres
# Vues concernant les matieres premieres
@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def mp_list(request):
    mps = MatierePremiere.objects.all()
    units = Unite.objects.all()
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            unit_name = request.POST.get('unit')
            critic_qts = int(request.POST.get('qts'))
            unit = Unite.objects.get(name=unit_name)
            type_mp = request.POST.get('type')
            MatierePremiere.objects.create(libelle=name, description=desc, unite=unit, critic_qts=critic_qts, type_mp=type_mp)
            messages.success(request, 'good !')
            return redirect('mp-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'bakery/mp_list.html', context={'mps': mps, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def mp_detail(request, pk):
    units = Unite.objects.all()
    mp = MatierePremiere.objects.get(pk=pk)

    if request.method == 'POST':
        if MatierePremiere.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            mp.libelle = request.POST.get('name')
            mp.description = request.POST.get('desc')
            mp.critic_qts = int(request.POST.get('qts'))
            mp.unit = Unite.objects.get(name=request.POST.get('unit'))
            mp.type_mp = request.POST.get('type')
            mp.save()
            messages.success(request, 'good !')
            return redirect('mp-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/mp_detail.html', context={'mp': mp, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_mp(request, pk):
    mp = MatierePremiere.objects.get(pk=pk)
    mp.delete()
    messages.success(request, 'good !')
    return redirect('mp-list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def entree_mp(request):
    mps = MatierePremiere.objects.all()
    entries = EntreeMp.objects.all().order_by('-id')
    date1 = None
    date2 = None
    p = Paginator(entries, 10)  # creating a paginator object
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            date_exp = request.POST.get('date_exp')
            price = int(request.POST.get('price'))
            devise = request.POST.get('devise')
            EntreeMp.objects.create(matiere_premiere=mp, qts=qts, date_exp=date_exp, price=price, devise=devise,
                                    taux=current_taux())
            messages.success(request, 'good !')
            return redirect('entree-mp')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreeMp.objects.filter(date=date1)
            p = Paginator(entries, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
        else:
            entries = EntreeMp.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
            p = Paginator(entries, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
    return render(request, 'bakery/entree_mp.html',
                  context={'mps': mps, 'page_obj': page_obj, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def sortie_mp(request):
    mps = MatierePremiere.objects.all()
    outs = SortieMp.objects.all().order_by('-id')
    date1 = None
    date2 = None
    p = Paginator(outs, 10)  # creating a paginator object
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            destination = request.POST.get('destination')
            if mp.in_stock >= qts:
                SortieMp.objects.create(matiere_premiere=mp, qts=qts, destination=destination)
                messages.success(request, 'good !')
                return redirect('sortie-mp')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-mp')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortieMp.objects.filter(date=date1)
            p = Paginator(outs, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
        else:
            outs = SortieMp.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
            p = Paginator(outs, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
    return render(request, 'bakery/sortie_mp.html', context={'mps': mps, 'page_obj': page_obj, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def edit_entree_mp(request, pk):
    entry = EntreeMp.objects.get(pk=pk)
    if request.method == 'POST':
        entry.date_exp = request.POST.get('date_exp')
        entry.save()
        messages.success(request, 'good !')
        return redirect('entree-mp')
    return render(request, 'bakery/forms/mp_entree_detail.html', context={'entry': entry})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_entree(request, pk):
    EntreeMp.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-mp')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_sortie(request, pk):
    SortieMp.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-mp')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def cmd_mp(request):
    orders = CommandeMp.objects.all()
    ref = generate_unique_uid()
    return render(request, 'bakery/bakery_cmd_mp.html', context={'orders': orders, 'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_cmd(request, pk):
    order = CommandeMp.objects.get(pk=pk)
    order.delete()
    messages.success(request, 'good !')
    return redirect('cmd-mp')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def detail_cmd_mp(request, ref):
    order = CommandeMp.objects.get(ref=ref)
    lines = LigneCommandeMp.objects.filter(commande=order)

    return render(request, 'bakery/detail_cmd_mp.html', context={'lines': lines, 'order': order})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def add_cmd_mp(request, ref):
    order, created = CommandeMp.objects.get_or_create(ref=ref)
    lines = LigneCommandeMp.objects.filter(commande=order)
    suppliers = Fournisseur.objects.all()
    mps = MatierePremiere.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier_name = request.POST.get('supplier')
        order.fournisseur = Fournisseur.objects.get(name=supplier_name)
        devise = request.POST.get('devise')
        order.devise = devise
        order.save()
        total_price = request.POST.get('price')
        qts = request.POST.get('qts')

        if MatierePremiere.objects.filter(libelle=name).count() > 0:
            mp = MatierePremiere.objects.get(libelle=name)
            line, created = LigneCommandeMp.objects.get_or_create(commande=order, matiere_premiere=mp)
            line.qts += int(qts)
            line.total_price += int(total_price)
            line.taux = current_taux()
            line.devise = devise
            line.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'bakery/add-line-cmd-mp.html',
                  context={'order': order, 'mps': mps, 'lines': lines, 'fournisseurs': suppliers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_line_cmd_mp(request, pk):
    line = LigneCommandeMp.objects.get(pk=pk)
    line.delete()
    messages.success(request, "good")
    return redirect('add-cmd-mp', line.commande.ref)


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def edit_line_cmd_mp(request, pk):
    line = LigneCommandeMp.objects.get(pk=pk)
    if request.method == 'POST':
        qts = int(request.POST.get('qts'))
        price = request.POST.get('price')
        line.qts = qts
        line.total_price = price
        line.save()
        messages.success(request, "good !")
        return redirect('add-cmd-mp', line.commande.ref)
    return render(request, 'bakery/forms/line_cmd_mp.html', context={'line': line})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def confirm_cmd_mp(request, ref):
    order = CommandeMp.objects.get(ref=ref)
    order.etat = True
    order.delivered_at = datetime.datetime.today().date()
    order.save()
    lines = LigneCommandeMp.objects.filter(commande=order)

    for line in lines:
        mp = line.matiere_premiere
        qts = line.qts
        price = line.total_price
        devise = order.devise
        EntreeMp.objects.create(matiere_premiere=mp, qts=qts, price=price, devise=devise, taux=current_taux())
        messages.success(request, 'good !')

    return redirect('cmd-mp')


# Vues concernant les produits finis
# Vues concernant les produits finis
# Vues concernant les produits finis

@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def pf_list(request):
    pfs = ProduitFini.objects.all()
    units = Unite.objects.all()
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            unit_name = request.POST.get('unit')
            critic_qts = int(request.POST.get('qts'))
            price = int(request.POST.get('price'))
            unit = Unite.objects.get(name=unit_name)
            type_prod = request.POST.get('type')
            ProduitFini.objects.create(libelle=name, description=desc, price=price, unite=unit, critic_qts=critic_qts, type_produit=type_prod)
            messages.success(request, 'good !')
            return redirect('pf-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'bakery/pf_list.html', context={'pfs': pfs, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def pf_detail(request, pk):
    units = Unite.objects.all()
    pf = ProduitFini.objects.get(pk=pk)
    if request.method == 'POST':
        if ProduitFini.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            pf.libelle = request.POST.get('name')
            pf.description = request.POST.get('desc')
            pf.critic_qts = int(request.POST.get('qts'))
            pf.price = int(request.POST.get('price'))
            pf.type_produit = request.POST.get('type')
            pf.unit = Unite.objects.get(name=request.POST.get('unit'))
            pf.save()
            messages.success(request, 'good !')
            return redirect('pf-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/pf_detail.html', context={'pf': pf, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_pf(request, pk):
    pf = ProduitFini.objects.get(pk=pk)
    pf.delete()
    messages.success(request, 'good !')
    return redirect('pf-list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def invendu_pf(request):
    pfs = ProduitFini.objects.all()
    invendus = InvenduPf.objects.all().order_by('-id')
    total_chf = 0
    chiffre_affaire, create = ChiffreAffaire.objects.get_or_create(date=datetime.datetime.today().date())
    outs = SortiePF.objects.filter(date=datetime.datetime.today().date())

    for o in outs:
        total_chf += o.total_cost
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).exists():
            pf = ProduitFini.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            date = request.POST.get('date')
            invendu, create = InvenduPf.objects.get_or_create(produit_fini=pf, date=datetime.datetime.today().date())
            invendu.qts += qts
            invendu.price = invendu.qts * pf.price
            invendu.date = date
            invendu.save()
            total_chf -= invendu.price
            chiffre_affaire.total_price = total_chf
            chiffre_affaire.save()
            messages.success(request, 'good !')
            return redirect('invendu-pf')
        else:
            messages.error(request, 'echec !')

    return render(request, 'bakery/invendu_pf.html',
                  context={'pfs': pfs, 'invendus': invendus})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_invendu_pf(request, pk):
    chiffre_affaire = ChiffreAffaire.objects.get_or_create(date=datetime.datetime.today().date())
    invendu = InvenduPf.objects.get(pk=pk)
    chiffre_affaire.total_price -= invendu.price
    invendu.delete()
    chiffre_affaire.save()
    messages.success(request, 'good !')
    return redirect('invendu-pf')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def entree_pf(request):
    pfs = ProduitFini.objects.all()
    entries = EntreePF.objects.all().order_by('-id')
    date1 = None
    date2 = None
    p = Paginator(entries, 10)  # creating a paginator object
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).exists():
            pf = ProduitFini.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            EntreePF.objects.create(produit_fini=pf, qts=qts)
            messages.success(request, 'good !')
            return redirect('entree-pf')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreePF.objects.filter(date=date1)
            p = Paginator(entries, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
        else:
            entries = EntreePF.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
            p = Paginator(entries, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
    return render(request, 'bakery/entree_pf.html',
                  context={'pfs': pfs, 'page_obj': page_obj, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def sortie_pf(request):
    pfs = ProduitFini.objects.all()
    outs = SortiePF.objects.all().order_by('-id')
    date1 = None
    date2 = None
    p = Paginator(outs, 10)  # creating a paginator object
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).exists():
            pf = ProduitFini.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if pf.in_stock >= qts:
                SortiePF.objects.create(produit_fini=pf, qts=qts, price=pf.price)
                messages.success(request, 'good !')
                return redirect('sortie-pf')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-pf')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortiePF.objects.filter(date=date1)
            p = Paginator(outs, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
        else:
            outs = SortiePF.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
            p = Paginator(outs, 10)  # creating a paginator object
            page_number = request.GET.get('page')
            try:
                page_obj = p.get_page(page_number)  # returns the desired page object
            except PageNotAnInteger:
                # if page_number is not an integer then assign the first page
                page_obj = p.page(1)
            except EmptyPage:
                # if page is empty then return last page
                page_obj = p.page(p.num_pages)
    return render(request, 'bakery/sortie_pf.html', context={'pfs': pfs, 'page_obj': page_obj, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_entree_pf(request, pk):
    EntreePF.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-pf')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_sortie_pf(request, pk):
    sortie = SortiePF.objects.get(pk=pk)
    try:
        entree = EntreePfPt.objects.get(added_at=sortie.added_at)
        entree.delete()
    except ObjectDoesNotExist:
        print("Impossible")
    sortie.delete()
    messages.success(request, 'good !')
    return redirect('sortie-pf')


# Vues concernant les fournitures
# Vues concernant les fournitures
# Vues concernant les fournitures

@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def fourniture_list(request):
    fournitures = Fourniture.objects.all()
    units = Unite.objects.all()
    if request.method == 'POST':
        if Fourniture.objects.filter(libelle=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            unit_name = request.POST.get('unit')
            unit = Unite.objects.get(name=unit_name)
            critic_qts = int(request.POST.get('qts'))
            Fourniture.objects.create(libelle=name, description=desc, unite=unit, critic_qts=critic_qts)
            messages.success(request, 'good !')
            return redirect('fourniture-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'bakery/fourniture_list.html', context={'fournitures': fournitures, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def fourniture_detail(request, pk):
    units = Unite.objects.all()
    fourniture = Fourniture.objects.get(pk=pk)

    if request.method == 'POST':
        if Fourniture.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            fourniture.libelle = request.POST.get('name')
            fourniture.description = request.POST.get('desc')
            fourniture.unit = Unite.objects.get(name=request.POST.get('unit'))
            fourniture.critic_qts = int(request.POST.get('qts'))
            fourniture.save()
            messages.success(request, 'good !')
            return redirect('fourniture-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/fourniture_detail.html', context={'fourniture': fourniture, 'units': units})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_fourniture(request, pk):
    fourniture = Fourniture.objects.get(pk=pk)
    fourniture.delete()
    messages.success(request, 'good !')
    return redirect('mp-list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def entree_fourniture(request):
    fournitures = Fourniture.objects.all()
    entries = EntreeFourniture.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if Fourniture.objects.filter(libelle=request.POST.get('name')).exists():
            fourniture = Fourniture.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            price = int(request.POST.get('price'))
            devise = request.POST.get('devise')
            EntreeFourniture.objects.create(fourniture=fourniture, qts=qts, price=price, devise=devise,
                                            taux=current_taux())
            messages.success(request, 'good !')
            return redirect('entree-fourniture')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreeFourniture.objects.filter(date=date1)
        else:
            entries = EntreeFourniture.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'bakery/entree_fourniture.html',
                  context={'fournitures': fournitures, 'entries': entries, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def sortie_fourniture(request):
    fournitures = Fourniture.objects.all()
    outs = SortieFourniture.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if Fourniture.objects.filter(libelle=request.POST.get('name')).exists():
            fourniture = Fourniture.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if fourniture.in_stock >= qts:
                SortieFourniture.objects.create(fourniture=fourniture, qts=qts)
                messages.success(request, 'good !')
                return redirect('sortie-fourniture')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-fourniture')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortieFourniture.objects.filter(date=date1)
        else:
            outs = SortieFourniture.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'bakery/sortie_fourniture.html',
                  context={'fournitures': fournitures, 'outs': outs, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_entree_fourniture(request, pk):
    EntreeFourniture.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-fourniture')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_sortie_fourniture(request, pk):
    SortieFourniture.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-fourniture')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def cmd_fourniture(request):
    orders = CommandeFourniture.objects.all()
    ref = generate_unique_uid()
    return render(request, 'bakery/cmd_fourniture.html', context={'orders': orders, 'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_cmd_fourniture(request, pk):
    order = CommandeFourniture.objects.get(pk=pk)
    order.delete()
    messages.success(request, 'good !')
    return redirect('cmd-fourniture')


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def detail_cmd_fourniture(request, ref):
    order = CommandeFourniture.objects.get(ref=ref)
    lines = LigneCommandeFourniture.objects.filter(commande=order)

    return render(request, 'bakery/detail_cmd_fourniture.html', context={'lines': lines, 'order': order})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def add_cmd_fourniture(request, ref):
    order, created = CommandeFourniture.objects.get_or_create(ref=ref)
    lines = LigneCommandeFourniture.objects.filter(commande=order)
    suppliers = Fournisseur.objects.all()
    fournitures = Fourniture.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        supplier_name = request.POST.get('supplier')
        order.fournisseur = Fournisseur.objects.get(name=supplier_name)
        devise = request.POST.get('devise')
        order.devise = devise
        order.save()
        total_price = request.POST.get('price')
        qts = request.POST.get('qts')

        if Fourniture.objects.filter(libelle=name).count() > 0:
            fourniture = Fourniture.objects.get(libelle=name)
            line, created = LigneCommandeFourniture.objects.get_or_create(commande=order, fourniture=fourniture)
            line.qts += int(qts)
            line.total_price += int(total_price)
            line.devise = devise
            line.taux = current_taux()
            line.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'bakery/add_line_cmd_fourniture.html',
                  context={'order': order, 'fournitures': fournitures, 'lines': lines, 'fournisseurs': suppliers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_line_cmd_fourniture(request, pk):
    line = LigneCommandeFourniture.objects.get(pk=pk)
    line.delete()
    messages.success(request, "good")
    return redirect('add-cmd-fourniture', line.commande.ref)


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def edit_line_cmd_fourniture(request, pk):
    line = LigneCommandeFourniture.objects.get(pk=pk)
    if request.method == 'POST':
        qts = int(request.POST.get('qts'))
        price = request.POST.get('price')
        line.qts = qts
        line.total_price = price
        line.save()
        messages.success(request, "good !")
        return redirect('add-cmd-fourniture', line.commande.ref)
    return render(request, 'bakery/forms/line_cmd_fourniture.html', context={'line': line})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def confirm_cmd_fourniture(request, ref):
    order = CommandeFourniture.objects.get(ref=ref)
    order.etat = True
    order.delivered_at = datetime.datetime.today().date()
    order.save()
    lines = LigneCommandeFourniture.objects.filter(commande=order)

    for line in lines:
        fourniture = line.fourniture
        qts = line.qts
        price = line.total_price
        devise = order.devise
        EntreeFourniture.objects.create(fourniture=fourniture, qts=qts, price=price, devise=devise, taux=current_taux())
        messages.success(request, 'good !')

    return redirect('cmd-fourniture')


# Vues concernant les fournisseurs


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    if request.method == 'POST':
        if Fournisseur.objects.filter(name=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            mail = request.POST.get('mail')
            address = request.POST.get('adresse')
            Fournisseur.objects.create(name=name, phone=phone, email=mail, address=address)
            messages.success(request, 'good !')
            return redirect('fournisseur-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/fournisseur_list.html', context={'fournisseurs': fournisseurs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def fournisseur_detail(request, pk):
    fournisseur = Fournisseur.objects.get(pk=pk)
    if request.method == 'POST':
        if Fournisseur.objects.exclude(pk=pk).filter(name=request.POST.get('name')).count() == 0:
            fournisseur.name = request.POST.get('name')
            fournisseur.phone = request.POST.get('phone')
            fournisseur.email = request.POST.get('mail')
            fournisseur.address = request.POST.get('adresse')
            fournisseur.save()
            messages.success(request, 'good !')
            return redirect('fournisseur-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/fournisseur_detail.html', context={'fournisseur': fournisseur})


@login_required(login_url='login')
@allowed_users(allowed_roles=['grand stock et boulangerie'])
def delete_fournisseur(request, pk):
    fournisseur = Fournisseur.objects.get(pk=pk)
    fournisseur.delete()
    messages.success(request, 'good !')
    return redirect('fournisseur-list')


# Vue concernants les alertes
# Vue concernants les alertes
# Vue concernants les alertes
def is_order_mp(mp: MatierePremiere):
    orders = CommandeMp.objects.filter(etat=False)
    for o in orders:
        lines = LigneCommandeMp.objects.filter(commande=o)
        for line in lines:
            if line.matiere_premiere == mp:
                return True
    return False


def is_order_fourniture(fourniture: Fourniture):
    orders = CommandeFourniture.objects.filter(etat=False)
    for o in orders:
        lines = LigneCommandeFourniture.objects.filter(commande=o)
        for line in lines:
            if line.fourniture == fourniture:
                return True
    return False


@login_required(login_url='login')
def check_critics(request):
    mps = MatierePremiere.objects.all()
    pfs = ProduitFini.objects.all()
    fournitures = Fourniture.objects.all()
    entries = EntreeMp.objects.filter(date_exp__isnull=False)
    expirations = []
    critic_mps = []
    critic_pfs = []
    critic_fournitures = []
    count = 0
    for e in entries:
        if 30 >= e.get_expiration_days >= 0:
            expirations.append(e)
            print(e.matiere_premiere.libelle + " " + str(e.get_expiration_days))
            count += 1

    for mp in mps:
        if mp.in_stock <= mp.critic_qts and is_order_mp(mp) is False:
            critic_mps.append(mp)
            count += 1
    for pf in pfs:
        if pf.in_stock <= pf.critic_qts:
            critic_pfs.append(pf)
            count += 1
    for fo in fournitures:
        if fo.in_stock <= fo.critic_qts and is_order_fourniture(fo) is False:
            critic_fournitures.append(fo)
            count += 1
    return render(request, 'bakery/partials/alert-critic.html', context={'count': count})


@login_required(login_url='login')
def stop_critics(request):
    return HttpResponse(status=286)


@login_required(login_url='login')
def check_notifications(request):
    mps = MatierePremiere.objects.all()
    pfs = ProduitFini.objects.all()
    fournitures = Fourniture.objects.all()
    entries = EntreeMp.objects.filter(date_exp__isnull=False, is_read_expired=False)
    critic_mps = []
    critic_pfs = []
    critic_fournitures = []
    expirations = []

    for e in entries:
        if 30 >= e.get_expiration_days >= 0:
            expirations.append(e)

    for mp in mps:
        if mp.in_stock <= mp.critic_qts and is_order_mp(mp) is False:
            critic_mps.append(mp)
    for pf in pfs:
        if pf.in_stock <= pf.critic_qts:
            critic_pfs.append(pf)
    for fo in fournitures:
        if fo.in_stock <= fo.critic_qts and is_order_fourniture(fo) is False:
            critic_fournitures.append(fo)
    return render(request, 'bakery/partials/notifications.html',
                  context={'critic_mps': critic_mps, 'critic_pfs': critic_pfs,
                           'critic_fournitures': critic_fournitures, 'expirations': expirations})


@login_required(login_url='login')
def notification_has_read(request, pk):
    e = EntreeMp.objects.get(pk=pk)
    e.is_read_expired = True
    e.save()
    return HttpResponse("")
