from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import Project
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import HIT

import logging

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class ViewHitPage(View):
    def get(self, request, *args, **kwargs):
        hit_id = self.kwargs['hit_id']
        hit = HIT.objects.get(pk=hit_id)
        headers = []
        for header in hit.project.csv_header:
        	headers.append(header+"_A")
        for header in hit.project.csv_header:
        	headers.append(header+"_B")
        	
        return render(request, 'view_hit.html', {'hit': hit, 'project': hit.project, 'headers': headers })
