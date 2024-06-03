from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
import datetime
from django.contrib.auth.decorators import login_required
from auth_user.decorators import allowed_users

# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def home_foodpack(request):
    return render(request, 'foodpack/home_pack.html', context={})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def pack_list(request):
    packs = FoodPack.objects.all()
    if request.method == 'POST':
        if FoodPack.objects.filter(libelle=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            price = int(request.POST.get('price'))
            FoodPack.objects.create(libelle=name, description=desc, price=price)
            messages.success(request, 'good !')
            return redirect('pack-list')
        else:
            messages.error(request, 'echec !')

    return render(request, 'foodpack/pack_list.html', context={'packs': packs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def pack_detail(request, pk):
    pack = FoodPack.objects.get(pk=pk)
    if request.method == 'POST':
        if FoodPack.objects.exclude(pk=pk).filter(libelle=request.POST.get('name')).count() == 0:
            pack.libelle = request.POST.get('name')
            pack.description = request.POST.get('desc')
            pack.price = int(request.POST.get('price'))
            pack.save()
            messages.success(request, 'good !')
            return redirect('pack-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'foodpack/forms/pack_detail.html', context={'pack': pack})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_pack(request, pk):
    pack = FoodPack.objects.get(pk=pk)
    pack.delete()
    messages.success(request, 'good !')
    return redirect('pack-list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def entree_pack(request):
    packs = FoodPack.objects.all()
    entries = EntreePack.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if FoodPack.objects.filter(libelle=request.POST.get('name')).exists():
            pack = FoodPack.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            EntreePack.objects.create(pack=pack, qts=qts)
            messages.success(request, 'good !')
            return redirect('entree-pack')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreePack.objects.filter(date=date1)
        else:
            entries = EntreePack.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'foodpack/entree_pack.html',
                  context={'packs': packs, 'entries': entries, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def sortie_pack(request):
    packs = FoodPack.objects.all()
    outs = SortiePack.objects.all().order_by('-id')
    entreprises = Entreprise.objects.all()
    date1 = None
    date2 = None
    if request.method == 'POST':
        if FoodPack.objects.filter(libelle=request.POST.get('name')).exists():
            pack = FoodPack.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            entreprise = Entreprise.objects.get(name=request.POST.get('entreprise'))

            if pack.in_stock >= qts:
                SortiePack.objects.create(pack=pack, qts=qts, entreprise=entreprise)
                messages.success(request, 'good !')
                return redirect('sortie-pack')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-pack')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortiePack.objects.filter(date=date1)
        else:
            outs = SortiePack.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'foodpack/sortie_pack.html',
                  context={'packs': packs, 'outs': outs, 'date1': date1, 'date2': date2, 'entreprises': entreprises})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_entree_pack(request, pk):
    EntreePack.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-pack')


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_sortie_pack(request, pk):
    SortiePack.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-pack')


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def invendu_pack(request):
    packs = FoodPack.objects.all()
    invendus = InvenduPack.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if FoodPack.objects.filter(libelle=request.POST.get('name')).exists():
            pack = FoodPack.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            date = request.POST.get('date')
            invendu, create = InvenduPack.objects.get_or_create(pack=pack, date=datetime.datetime.today().date())
            invendu.qts += qts
            invendu.price = invendu.qts * pack.price
            invendu.date = date
            invendu.save()
            EntreePack.objects.create(pack=pack, qts=invendu.qts)
            messages.success(request, 'good !')
            return redirect('invendu-pack')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            invendus = InvenduPack.objects.filter(date=date1)
        else:
            invendus = InvenduPack.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'foodpack/retour_pack.html',
                  context={'packs': packs, 'invendus': invendus, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_invendu_pack(request, pk):
    invendu = InvenduPack.objects.get(pk=pk)
    invendu.delete()
    messages.success(request, 'good !')
    return redirect('invendu-pack')


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def entreprise_list(request):
    entreprises = Entreprise.objects.all()
    if request.method == 'POST':
        if Entreprise.objects.filter(name=request.POST.get('name')).count() == 0:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            mail = request.POST.get('mail')
            address = request.POST.get('adresse')
            Entreprise.objects.create(name=name, phone=phone, mail=mail, adresse=address)
            messages.success(request, 'good !')
            return redirect('entreprise-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'foodpack/entreprises.html', context={'entreprises': entreprises})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def entreprise_detail(request, pk):
    entreprise = Entreprise.objects.get(pk=pk)
    if request.method == 'POST':
        if Entreprise.objects.exclude(pk=pk).filter(name=request.POST.get('name')).count() == 0:
            entreprise.name = request.POST.get('name')
            entreprise.phone = request.POST.get('phone')
            entreprise.mail = request.POST.get('mail')
            entreprise.adresse = request.POST.get('adresse')
            entreprise.save()
            messages.success(request, 'good !')
            return redirect('entreprise-list')
        else:
            messages.error(request, 'echec !')
    return render(request, 'foodpack/forms/entreprise_detail.html', context={'entreprise': entreprise})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_entreprise(request, pk):
    entreprise = Entreprise.objects.get(pk=pk)
    entreprise.delete()
    messages.success(request, 'good !')
    return redirect('entreprise-list')


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def mp_list_pack(request):
    mps1 = []
    for i in MatierePremiere.objects.all():
        for j in EntreeMpPack.objects.all():
            if i == j.matiere_premiere:
                mps1.append(j.matiere_premiere.libelle)
        if i.type_mp in ['BOULANGERIE ET PACK', 'PACK']:
            mps1.append(i.libelle)
    mps = MatierePremiere.objects.filter(libelle__in=mps1)

    return render(request, 'foodpack/mp_list.html', context={'mps': mps})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def entree_mp_pack(request):
    mps1 = []
    for i in MatierePremiere.objects.all():
        for j in EntreeMpPack.objects.all():
            if i == j.matiere_premiere:
                mps1.append(j.matiere_premiere.libelle)
        if i.type_mp in ['BOULANGERIE ET PACK', 'PACK']:
            mps1.append(i.libelle)
    mps = MatierePremiere.objects.filter(libelle__in=mps1)
    entries = EntreeMpPack.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            EntreeMpPack.objects.create(matiere_premiere=mp, qts=qts)
            messages.success(request, 'good !')
            return redirect('entree-mp-pack')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            entries = EntreeMpPack.objects.filter(date=date1)
        else:
            entries = EntreeMpPack.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'foodpack/entree_mp.html',
                  context={'mps': mps, 'entries': entries, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def sortie_mp_pack(request):
    mps = MatierePremiere.objects.filter(type_mp__in=['BOULANGERIE ET PACK', 'PACK'])
    outs = SortieMpPack.objects.all().order_by('-id')
    date1 = None
    date2 = None
    if request.method == 'POST':
        if MatierePremiere.objects.filter(libelle=request.POST.get('name')).exists():
            mp = MatierePremiere.objects.get(libelle=request.POST.get('name'))
            qts = int(request.POST.get('qts'))
            if mp.in_stock_pack >= qts:
                SortieMpPack.objects.create(matiere_premiere=mp, qts=qts)
                messages.success(request, 'good !')
                return redirect('sortie-mp-pack')
            else:
                messages.error(request, 'stock !')
                return redirect('sortie-mp-pack')
        else:
            messages.error(request, 'echec !')
    if request.GET.get('search') is not None:
        date1 = request.GET.get('date1')
        date2 = request.GET.get('date2')
        if date2 == "" or date2 is None:
            outs = SortieMpPack.objects.filter(date=date1)
        else:
            outs = SortieMpPack.objects.filter(Q(date__gte=date1) & Q(date__lte=date2))
    return render(request, 'foodpack/sortie_mp.html', context={'mps': mps, 'outs': outs, 'date1': date1, 'date2': date2})


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_entree_pack(request, pk):
    EntreeMpPack.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('entree-mp-pack')


@login_required(login_url='login')
@allowed_users(allowed_roles=['livraison de pack'])
def delete_sortie_pack(request, pk):
    SortieMpPack.objects.get(pk=pk).delete()
    messages.success(request, 'good !')
    return redirect('sortie-mp-pack')


