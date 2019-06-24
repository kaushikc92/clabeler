from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import Project, HIT

import logging

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class ViewProjectPage(View):
    def get(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(pk=project_id)
        hits = HIT.objects.filter(project_id=project_id)
        return render(request, 'view_project.html', {'project': project, 'hits': hits })
