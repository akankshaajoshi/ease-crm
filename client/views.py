import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client
from .forms import AddClientForm, AddCommentForm, AddFileForm
from team.models import Team
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def clients_export(request):
    clients = Client.objects.filter(created_by=request.user)
    response = HttpResponse(
        content_type="text/csv",
        headers={'Content-Disposition': "attachment; filename='clients.csv'"},
    )
    writer = csv.writer(response)
    writer.writerow(['Client', 'Description', 'Created At', 'Created By'])
    for client in clients:
        writer.writerow([client.name, client.description, client.created_at, client.created_by])
    return response


@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    return render(request, 'client/clients_list.html', {
        'clients': clients
    })

@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, pk = pk, created_by = request.user)
    if request.method == "POST":
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.active_team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)
        
    else:
        form = AddCommentForm();
    return render(request, 'client/clients_detail.html', {
        'client': client,
        'form': form,
        'fileform': AddFileForm()
    })


@login_required
def clients_add(request):
    team = request.user.userprofile.active_team

    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = request.user.userprofile.active_team
            client.save()

            messages.success(request, "Client has been added.")
            return redirect('clients:list')
    else:
        form = AddClientForm()
    return render(request, 'client/clients_add.html', {
            'form': form,
            'team': team,
        })

@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, pk = pk, created_by = request.user)
    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Client has been updated.")
            return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)
    
    return render(request, 'client/clients_edit.html', {'form': form})

@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, pk = pk, created_by = request.user)
    client.delete()
    messages.success(request, "Client has been deleted.")
    return redirect('clients:list')


@login_required
def clients_add_file(request, pk):
    client = get_object_or_404(Client, pk = pk, created_by = request.user)

    if request.method == "POST":
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.team = request.user.userprofile.active_team
            file.client_id = pk
            file.created_by = request.user
            file.save()

        return redirect("clients:detail", pk=pk)
    return redirect("clients:detail", pk=pk)
    