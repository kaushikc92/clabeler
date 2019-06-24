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
class ProjectActionsPage(View):
    def get(self, request, *args, **kwargs):
        # return render(request, 'project_actions.html')
        username = request.user.username
        user = User.objects.get(username=username)
        
        success_bool = '-1'
        if 'success' in self.kwargs:
            # import pdb; pdb.set_trace()
            if self.kwargs['success']:
                success_bool = self.kwargs['success']
            else:
                success_bool = '0'
       

        if user:
            owner = UserProfile.objects.get(user = user)
            projects = Project.objects.filter(owner=owner)
            return render(request, 'project_actions.html', {'projects': projects, 'success':success_bool })

    def post(self, request, *args, **kwargs):
        pass