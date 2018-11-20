from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from pedais.models import Pedal, Grupo
from pedais.forms import PedalForm, PedalExistenteNoGrupoForm


def home_page(request):
    return render(request,'home.html', {'form':PedalForm()})


def view_grupo(request, grupo_id):
    grupo = Grupo.objects.get(id=grupo_id)
    form = PedalExistenteNoGrupoForm(grupo=grupo)

    if request.method == 'POST':
        form = PedalExistenteNoGrupoForm(data=request.POST, grupo=grupo)
        if form.is_valid():
            form.save()
            return redirect(grupo)
    return render(request, 'grupo.html',{'grupo':grupo, 'form':form})

def novo_grupo(request):
    form = PedalForm(data=request.POST)
    if form.is_valid():
        grupo = Grupo.objects.create()
        form.save(grupo=grupo)
        return redirect(grupo)
    return render(request, 'home.html', {'form':form})
