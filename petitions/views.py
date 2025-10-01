from django.shortcuts import render, redirect, get_object_or_404
from .models import Petition
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser


def index(request):
    template_data = {}
    petitions = Petition.objects.all()
    pdata = []
    for petition in petitions:
        has_signed = False

        if not isinstance(request.user, AnonymousUser):
            has_signed = request.user in petition.signers.all()

        # We're checking has_signed server-side so that we don't expose
        # the entire list of petitioners to the front end, in case we'd have privacy issues
        pdata.append({
            'id': petition.id,
            'movie_name': petition.movie_name,
            'creator': petition.creator,
            'signers_count': petition.signers.count(),
            'has_signed': has_signed
        })

    template_data['petitions'] = pdata
    return render(request, "petitions/index.html", {"template_data": template_data})


@login_required
def create(request):
    if request.method == "POST" and request.POST["movie_name"] != "":
        petition = Petition()
        petition.movie_name = request.POST["movie_name"]
        petition.creator = request.user
        petition.save()

    return redirect("petitions.index")


@login_required
def sign(request, id):
    petition = get_object_or_404(Petition, id=id)
    petition.signers.add(request.user)
    petition.save()

    return redirect("petitions.index")
