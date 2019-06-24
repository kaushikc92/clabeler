from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import Project
from labeling.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

import logging


logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class IndexPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    # def get(self, request, *args, **kwargs):
    #     username = request.user.username
    #     user = User.objects.get(username=username)
    #     if user:
    #         worker = UserProfile.objects.get(user=user)
    #     else:
    #         worker = None
    #     projects = self.target(worker)
    #     #projects = Project.objects.filter(owner=owner)
    #     return render(request, 'project.html', {'projects': projects })

    # def target(self, worker):
    #     """ target worker with user profiles and project settings """
    #     # age, gender, location, career, approval_rate, approval_HIT_number
    #     ages = [i[0] for i in AGE_CHOICES if worker.age <= i[1][1] and worker.age >= i[1][0]]
    #     age = ages[0] if ages else 0
    #     projects = Project.objects.filter(Q(age = age) | Q(age = 0),
    #             Q(gender = worker.gender) | Q(gender = 0),
    #             Q(location = worker.location) | Q(location = 0),
    #             Q(career = worker.career) | Q(career = 0),
    #             Q(approval_rate__lte = worker.approval_rate) | Q(approval_rate = 0),
    #             Q(approval_HIT_number__lte = worker.approval_HIT_number) | Q(approval_HIT_number = 0))
    #     return projects
