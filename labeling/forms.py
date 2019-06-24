from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import AuthenticationForm
import re


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Please enter a username'}))
    password1 = forms.CharField(label='Password',
                                max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please enter a password'}))
    password2 = forms.CharField(label='Re-enter password',
                                max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please reenter your password'}))
    email = forms.EmailField(label='Email', required=True)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(
                'Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class CreateProjectForm(forms.Form):

    def __init__(self, *args, **kwargs):

        self.gender_choices = kwargs.pop('gender_choices')
        self.age =  kwargs.pop('age')
        self.approval_hit_count_choices = kwargs.pop('approval_hit_count_choices')
        self.approval_rate = 0
        self.expiry_days_count = kwargs.pop('expiry_days_count')
        super(CreateProjectForm, self).__init__(*args, **kwargs)

        self.fields['project_name'] = forms.CharField(label='Project Name*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter project name'}))


        self.fields['worker_count'] = forms.CharField(label='Workers Count Per HIT*', max_length=200,
                                      help_text='Tooltip description goes here for title',
                                      widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter number of assignments per HIT'}))

        self.fields['tuples_count'] = forms.CharField(label='Tuple Count Per HIT*', max_length=200,
                                      help_text='Tooltip description goes here for title',
                                      widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter number of tuples per HIT'}))


        self.fields['worker_age'] = forms.ChoiceField( widget=forms.Select(),
                                            choices=self.age, initial=1, required=False)

                                              
        self.fields['description'] = forms.CharField(label='Description*', max_length=200,
                                            help_text='Tooltip description goes here for desc',
                                             widget=forms.Textarea(
                                              attrs={'type': 'text', 'class': "form-control", 'rows': "2", 'placeholder': 'Optionally, describe your project here'}))

       
        self.fields['name'] = forms.CharField(label='Project Name*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter Project Name'}))

        self.fields['approval_rate'] = forms.CharField(label='Approval rate*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter approval rate from 0-100'}))
        
        self.fields['expiry_days_count'] = forms.CharField(label='Project expiry in days*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter project expiry in days'}))
        
        
class UploadDatasetForm(forms.Form):

    def __init__(self, *args, **kwargs):

        select_options = []
        super(UploadDatasetForm, self).__init__(*args, **kwargs)

        self.fields['wfid'] = forms.CharField(label='Workflow ID',
                               max_length=100, required=True,)                   

        self.fields['fragid'] = forms.CharField(label='Fragment ID', max_length=100, required=True,)

        self.fields['description'] = forms.CharField(label='Description (optional)', max_length=100, required=False,
                                      widget=forms.Textarea(attrs={'placeholder': 'Optionally, describe your table here', 'rows': '4'}))

        self.fields['docfile'] = forms.FileField(label='Choose file')



class EditProjectParametersForm(forms.Form):

    def __init__(self, *args, **kwargs):

       
        super(EditProjectParametersForm, self).__init__(*args, **kwargs)

        self.fields['project_name'] = forms.CharField(label='Project Name*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter project name'}))

        self.fields['tuples_count'] = forms.CharField(label='Tuple Count Per HIT*', max_length=200,
                                      help_text='Tooltip description goes here for title',
                                      widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter number of tuples per HIT'}))  
                                              
        self.fields['description'] = forms.CharField(label='Description*', max_length=200,
                                            help_text='Tooltip description goes here for desc',
                                             widget=forms.Textarea(
                                              attrs={'type': 'text', 'class': "form-control", 'rows': "2", 'placeholder': 'Optionally, describe your project here'}))

       
        self.fields['name'] = forms.CharField(label='Project Name*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter Project Name'}))

        self.fields['expiry_days_count'] = forms.CharField(label='Project expiry in days*', max_length=200,
                                              help_text='Tooltip description goes here for title',
                                              widget=forms.TextInput(attrs={'type': 'text', 'class': "form-control", 'placeholder': 'Enter project expiry in days'}))
