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
class ReviewLabellingPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'review_labelling.html')
        
    