import csv
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,  DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from .models import Lead
from .forms import LeadForm, AddCommentForm, AddFileForm
from team.models import Team
from client.models import Client, Comment as ClientComment

class LeadListView(LoginRequiredMixin, ListView):
     model = Lead

     def get_queryset(self):
          queryset = super(LeadListView, self).get_queryset()
          return queryset.filter(created_by = self.request.user,converted_to_client=False )

class LeadDetailView(LoginRequiredMixin, DetailView):
     model = Lead

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs);
          context['form'] = AddCommentForm()
          context['fileform'] = AddFileForm()
          return context
     
     def get_queryset(self):
          queryset = super(LeadDetailView, self).get_queryset()
          return queryset.filter(created_by = self.request.user, pk = self.kwargs.get('pk'))


class LeadDeleteView(LoginRequiredMixin, DeleteView):
     model = Lead
     success_url = reverse_lazy('leads:list')

     def get_queryset(self):
          queryset = super(LeadDeleteView, self).get_queryset()
          return queryset.filter(created_by = self.request.user, pk = self.kwargs.get('pk'))

     def get(self, request, *args, **kwargs):
          return self.post(request, *args, **kwargs)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
     model = Lead
     fields = ('name', 'email', 'description', 'priority', 'status')
     success_url = reverse_lazy("leads:list")
 
     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs);
          context['title'] = "Edit Lead"
          return context
     
     def get_queryset(self):
          queryset = super(LeadUpdateView, self).get_queryset()
          return queryset.filter(created_by = self.request.user, pk = self.kwargs.get('pk'))
     

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    success_url = reverse_lazy("leads:list")

    def get_queryset(self):
        queryset = super(LeadCreateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context['team'] = team
        context['title'] = "Add Lead"
        return context

    def form_valid(self, form):
        team = self.request.user.userprofile.active_team
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
class AddFileView(LoginRequiredMixin, View):
     def post(self, request, *args, **kwargs):
          pk = kwargs.get('pk')
          form = AddFileForm(request.POST, request.FILES)
          if form.is_valid():
               team = self.request.user.userprofile.active_team
               file = form.save(commit=False)
               file.team = team
               file.lead_id = pk
               file.created_by = request.user
               file.save()
          return redirect('leads:detail', pk=pk)

class LeadExportView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
          leads = Lead.objects.all().filter(created_by=request.user, converted_to_client=False)
          response = HttpResponse(
          content_type="text/csv",
          headers={'Content-Disposition': "attachment; filename='leads.csv'"},
          )
          writer = csv.writer(response)
          writer.writerow(['Lead', 'Description', 'Created At', 'Created By'])
          for lead in leads:
               writer.writerow([lead.name, lead.description, lead.created_at, lead.created_by])
          return response

class AddCommentView(LoginRequiredMixin, View):
     def post(self, request, *args, **kwargs):
          pk = kwargs.get('pk')
          form = AddCommentForm(request.POST)
          if form.is_valid():
               team = self.request.user.userprofile.active_team
               comment = form.save(commit=False)
               comment.team = team
               comment.created_by = request.user
               comment.lead_id = pk
               comment.save()
          return redirect('leads:detail', pk= pk)
     
class ConvertToClientView(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
          lead = get_object_or_404(Lead, created_by=request.user, pk = self.kwargs.get('pk'))
          team = request.user.userprofile.active_team
          client = Client.objects.create(
          name=lead.name,
          email = lead.email,
          description = lead.description,
          created_by = request.user,
          team = team
          )
          lead.converted_to_client = True
          lead.save()

          # Convert lead comments to converted client comments
          comments = lead.comments.all()
          for comment in comments:
               ClientComment.objects.create(
                    content=comment.content,
                    client = client,
                    created_by = comment.created_by,
                    team = team,
               )
          messages.success(request, 'The lead was converted to a client.')
          return redirect('leads:list')

# @login_required
# def leads_list(request):
#      leads = Lead.objects.filter(converted_to_client = False,created_by = request.user)
#      return render(request, 'lead/leads_list.html', {
#          'leads': leads
#      })


# @login_required
# def leads_detail(request, pk):
#      lead = get_object_or_404(Lead, created_by = request.user, pk = pk)
#     #  lead = Lead.objects.filter(created_by=request.user).get(pk=pk)
#      return render(request, 'lead/leads_detail.html', {
#           'lead': lead
#      })


# @login_required
# def leads_edit(request, pk):
#      lead = get_object_or_404(Lead, created_by=request.user, pk = pk)
#      if request.method == "POST":
#           form = AddLeadForm(request.POST, instance=lead)
#           if form.is_valid():
#                form.save()

#           messages.success(request, 'The changes were saved.')
#           return redirect('leads:list')
#      else:
#           form = AddLeadForm(instance=lead)
#           return render(request, 'lead/leads_edit.html', {
#                'form': form
#           })

# @login_required
# def leads_delete(request, pk):
#      lead = get_object_or_404(Lead, created_by=request.user, pk = pk)
#      lead.delete()
#      messages.success(request, 'The lead was deleted.')
#      return redirect('leads:list')

# @login_required
# def add_lead(request):
#     team = Team.objects.filter(created_by=request.user)[0]
#     if request.method == 'POST':
#         form  = AddLeadForm(request.POST)
#         if form.is_valid():
#                 team = Team.objects.filter(created_by=request.user)[0]
#                 lead = form.save(commit = False)
#                 lead.created_by = request.user
#                 lead.team = team
#                 lead.save()
#                 messages.success(request, 'The lead was created.')
#                 return redirect('leads:list')
#     else:
#         form = AddLeadForm()
#     return render(request, 'lead/add_lead.html', {
#         'form': form,
#         'team': team
#     })

# @login_required
# def convert_to_client(request, pk):
#      lead = get_object_or_404(Lead, created_by=request.user, pk = pk)
#      team = Team.objects.filter(created_by=request.user)[0]
#      client = Client.objects.create(
#           name=lead.name,
#           email = lead.email,
#           description = lead.description,
#           created_by = request.user,
#           team = team
#      )
#      lead.converted_to_client = True
#      lead.save()
#      messages.success(request, 'The lead was converted to a client.')
#      return redirect('leads:list')
