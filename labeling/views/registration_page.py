from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from labeling.forms import RegistrationForm

import logging

logger = logging.getLogger(__name__)

class RegistrationPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'userreg/register.html')

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        success = False
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email'])
            success = True

        return render(request, 'userreg/register.html', {'form': form, 'success': success})
