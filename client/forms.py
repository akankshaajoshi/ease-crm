from django import forms
from .models import Client, Comment, ClientFile

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full  mt-4 my-4 py-4 px-6 rounded-xl bg-gray-100'}),
            'email': forms.EmailInput(attrs={'class': 'w-full  mt-4 my-4 py-4 px-6 rounded-xl bg-gray-100'}),
            'description': forms.TextInput(attrs={'class': 'w-full  mt-4 my-4 py-4 px-6 rounded-xl bg-gray-100'}),
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )

class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)