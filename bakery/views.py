import datetime
import decimal
from pathlib import Path
from time import strftime
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib import messages
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
import uuid


# Create your views here.


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


def home_bakery(request):
    print(Path(__file__).resolve().parent.parent)
    return render(request, 'bakery/home_bakery.html', context={})


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


def delete_unit(request, pk):
    unit = Unite.objects.get(pk=pk)
    unit.delete()
    messages.success(request, 'good !')
    return redirect('unit-list')


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
            MatierePremiere.objects.create(libelle=name, description=desc, unite=unit, critic_qts=critic_qts)
            messages.success(request, 'good !')
            return redirect('mp-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'bakery/mp_list.html', context={'mps': mps, 'units': units})


def mp_detail(request, pk):
    units = Unite.objects.all()
    mp = MatierePremiere.objects.get(pk=pk)

    if request.method == 'POST':
        if MatierePremiere.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            mp.libelle = request.POST.get('name')
            mp.description = request.POST.get('desc')
            mp.critic_qts = int(request.POST.get('qts'))
            mp.unit = Unite.objects.get(name=request.POST.get('unit'))
            mp.save()
            messages.success(request, 'good !')
            return redirect('mp-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/mp_detail.html', context={'mp': mp, 'units': units})


def delete_mp(request, pk):
    mp = MatierePremiere.objects.get(pk=pk)
    mp.delete()
    messages.success(request, 'good !')
    return redirect('mp-list')


def entree_mp(request):
    mps = MatierePremiere.objects.all()
    entries = EntreeMp.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            date_exp = request.POST.get('date_exp')
            price = int(request.POST.get('price'))
            devise = request.POST.get('devise')
            EntreeMp.objects.create(matiere_premiere=mp, qts=qts, date_exp=date_exp, price=price, devise=devise)
            messages.success(request, 'good !')
            return redirect('entree-mp')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreeMp.objects.filter(date=date1)
        else:
            entries = EntreeMp.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'bakery/entree_mp.html', context={'mps': mps, 'entries': entries, 'date1': date1, 'date2': date2})


def sortie_mp(request):
    mps = MatierePremiere.objects.all()
    outs = SortieMp.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if mp.in_stock >= qts:
                SortieMp.objects.create(matiere_premiere=mp, qts=qts)
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
        else:
            outs = SortieMp.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'bakery/sortie_mp.html', context={'mps': mps, 'outs': outs, 'date1': date1, 'date2': date2})


def edit_entree_mp(request, pk):
    entry = EntreeMp.objects.get(pk=pk)
    if request.method == 'POST':
        entry.date_exp = request.POST.get('date_exp')
        entry.save()
        messages.success(request, 'good !')
        return redirect('entree-mp')
    return render(request, 'bakery/forms/mp_entree_detail.html', context={'entry': entry})


def delete_entree(request, pk):
    EntreeMp.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-mp')


def delete_sortie(request, pk):
    SortieMp.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-mp')


def cmd_mp(request):
    orders = CommandeMp.objects.all()
    ref = generate_unique_uid()
    return render(request, 'bakery/bakery_cmd_mp.html', context={'orders': orders, 'ref': ref})


def delete_cmd(request, pk):
    order = CommandeMp.objects.get(pk=pk)
    order.delete()
    messages.success(request, 'good !')
    return redirect('cmd-mp')


def detail_cmd_mp(request, ref):
    order = CommandeMp.objects.get(ref=ref)
    lines = LigneCommandeMp.objects.filter(commande=order)

    return render(request, 'bakery/detail_cmd_mp.html', context={'lines': lines, 'order': order})


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
            line.devise = devise
            line.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'bakery/add-line-cmd-mp.html', context={'order': order, 'mps': mps, 'lines': lines, 'fournisseurs': suppliers})


def delete_line_cmd_mp(request, pk):
    line = LigneCommandeMp.objects.get(pk=pk)
    line.delete()
    messages.success(request, "good")
    return redirect('add-cmd-mp', line.commande.ref)


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


def confirm_cmd_mp(request, ref):
    order = CommandeMp.objects.get(ref=ref)
    order.etat = True
    order.save()
    lines = LigneCommandeMp.objects.filter(commande=order)

    for line in lines:
        mp = line.matiere_premiere
        qts = line.qts
        price = line.total_price
        devise = order.devise
        EntreeMp.objects.create(matiere_premiere=mp, qts=qts, price=price, devise=devise)
        messages.success(request, 'good !')

    return redirect('cmd-mp')


# Vues concernant les produits finis


def pf_list(request):
    pfs = ProduitFini.objects.all()
    units = Unite.objects.all()
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            unit_name = request.POST.get('unit')
            critic_qts = int(request.POST.get('qts'))
            unit = Unite.objects.get(name=unit_name)
            ProduitFini.objects.create(libelle=name, description=desc, unite=unit, critic_qts=critic_qts)
            messages.success(request, 'good !')
            return redirect('pf-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'bakery/pf_list.html', context={'pfs': pfs, 'units': units})


def pf_detail(request, pk):
    units = Unite.objects.all()
    pf = ProduitFini.objects.get(pk=pk)
    if request.method == 'POST':
        if ProduitFini.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            pf.libelle = request.POST.get('name')
            pf.description = request.POST.get('desc')
            pf.critic_qts = int(request.POST.get('qts'))
            pf.unit = Unite.objects.get(name=request.POST.get('unit'))
            pf.save()
            messages.success(request, 'good !')
            return redirect('pf-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'bakery/forms/pf_detail.html', context={'pf': pf, 'units': units})


def delete_pf(request, pk):
    pf = ProduitFini.objects.get(pk=pk)
    pf.delete()
    messages.success(request, 'good !')
    return redirect('pf-list')


def entree_pf(request):
    pfs = ProduitFini.objects.all()
    entries = EntreePF.objects.all().order_by('-id')
    date1 = None
    date2 = None
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
        else:
            entries = EntreePF.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'bakery/entree_pf.html', context={'pfs': pfs, 'entries': entries, 'date1': date1, 'date2': date2})


def sortie_pf(request):
    pfs = ProduitFini.objects.all()
    outs = SortiePF.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if ProduitFini.objects.filter(libelle=request.POST.get('name')).exists():
            pf = ProduitFini.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if pf.in_stock >= qts:
                SortiePF.objects.create(produit_fini=pf, qts=qts)
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
        else:
            outs = SortiePF.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'bakery/sortie_pf.html', context={'pfs': pfs, 'outs': outs, 'date1': date1, 'date2': date2})


def delete_entree_pf(request, pk):
    EntreePF.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-pf')


def delete_sortie_pf(request, pk):
    SortiePF.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-pf')


# Vues concernant les fournitures


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


def delete_fourniture(request, pk):
    fourniture = Fourniture.objects.get(pk=pk)
    fourniture.delete()
    messages.success(request, 'good !')
    return redirect('mp-list')


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
            EntreeFourniture.objects.create(fourniture=fourniture, qts=qts, price=price, devise=devise)
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
    return render(request, 'bakery/entree_fourniture.html', context={'fournitures': fournitures, 'entries': entries, 'date1': date1, 'date2': date2})


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
    return render(request, 'bakery/sortie_fourniture.html', context={'fournitures': fournitures, 'outs': outs, 'date1': date1, 'date2': date2})


def delete_entree_fourniture(request, pk):
    EntreeFourniture.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-fourniture')


def delete_sortie_fourniture(request, pk):
    SortieFourniture.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-fourniture')


def cmd_fourniture(request):
    orders = CommandeFourniture.objects.all()
    ref = generate_unique_uid()
    return render(request, 'bakery/cmd_fourniture.html', context={'orders': orders, 'ref': ref})


def delete_cmd_fourniture(request, pk):
    order = CommandeFourniture.objects.get(pk=pk)
    order.delete()
    messages.success(request, 'good !')
    return redirect('cmd-fourniture')


def detail_cmd_fourniture(request, ref):
    order = CommandeFourniture.objects.get(ref=ref)
    lines = LigneCommandeFourniture.objects.filter(commande=order)

    return render(request, 'bakery/detail_cmd_fourniture.html', context={'lines': lines, 'order': order})


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
            line.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'bakery/add_line_cmd_fourniture.html', context={'order': order, 'fournitures': fournitures, 'lines': lines, 'fournisseurs': suppliers})


def delete_line_cmd_fourniture(request, pk):
    line = LigneCommandeFourniture.objects.get(pk=pk)
    line.delete()
    messages.success(request, "good")
    return redirect('add-cmd-fourniture', line.commande.ref)


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


def confirm_cmd_fourniture(request, ref):
    order = CommandeFourniture.objects.get(ref=ref)
    order.etat = True
    order.save()
    lines = LigneCommandeFourniture.objects.filter(commande=order)

    for line in lines:
        fourniture = line.fourniture
        qts = line.qts
        price = line.total_price
        devise = order.devise
        EntreeFourniture.objects.create(fourniture=fourniture, qts=qts, price=price, devise=devise)
        messages.success(request, 'good !')

    return redirect('cmd-fourniture')

# Vues concernant les fournisseurs


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


def delete_fournisseur(request, pk):
    fournisseur = Fournisseur.objects.get(pk=pk)
    fournisseur.delete()
    messages.success(request, 'good !')
    return redirect('fournisseur-list')


# Vue concernants les alertes

def is_order_mp(mp:MatierePremiere):
    orders = CommandeMp.objects.filter(etat=False)
    for o in orders:
        lines = LigneCommandeMp.objects.filter(commande=o)
        for line in lines:
            if line.matiere_premiere == mp:
                return True
    return False


def is_order_fourniture(fourniture:Fourniture):
    orders = CommandeFourniture.objects.filter(etat=False)
    for o in orders:
        lines = LigneCommandeFourniture.objects.filter(commande=o)
        for line in lines:
            if line.fourniture == fourniture:
                return True
    return False


def check_critics(request):
    mps = MatierePremiere.objects.all()
    pfs = ProduitFini.objects.all()
    fournitures = Fourniture.objects.all()
    critic_mps = []
    critic_pfs = []
    critic_fournitures = []

    for mp in mps:
        if mp.in_stock <= mp.critic_qts and is_order_mp(mp) is False:
            critic_mps.append(mp)
    for pf in pfs:
        if pf.in_stock <= pf.critic_qts:
            critic_pfs.append(pf)
    for fo in fournitures:
        if fo.in_stock <= fo.critic_qts and is_order_fourniture(fo) is False:
            critic_fournitures.append(fo)

    return render(request, 'bakery/partials/alert-critic.html', context={'critic_mps': critic_mps, 'critic_pfs': critic_pfs, 'critic_fournitures': critic_fournitures})


def stop_critics(request):
    return HttpResponse(status=286)