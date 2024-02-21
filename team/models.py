from django.db import models
from django.contrib.auth.models import  User

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    max_leads = models.IntegerField()
    max_clients = models.IntegerField()

    def __str__(self):
        return self.name
# Create your models here.
    
class Team(models.Model):
    plan=models.ForeignKey(Plan, blank=True, null=True, related_name="teams", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name="created_teams", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="teams")

    def __str__(self):
        return self.name
    
