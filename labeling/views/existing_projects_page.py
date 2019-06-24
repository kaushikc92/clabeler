from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import Project
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import UserProfile
import logging


logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class ExistingProjectsPage(View):
    def get(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        # on_success = request.kwargs.get('creation_success', False)
       
        username = request.user.username
        user = User.objects.get(username=username)
        if user:
            owner = UserProfile.objects.get(user = user)
            projects = Project.objects.filter(owner=owner)
            return render(request, 'existing_projects.html', {'projects': projects })
        