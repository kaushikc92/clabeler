#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# File Name: workers_hits_page.py
"""
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import Project, UserProfile, HIT, Assignment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

import logging
import datetime

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class WorkersHitsPage(View):

    def get(self, request, *args, **kwargs):
        """
            1. filter worker using project parameters.
            2. separate resume and select pages.
        """
        username = request.user.username
        user = User.objects.get(username=username)
        if user:
            worker = UserProfile.objects.get(user=user)
        else:
            worker = None
        projects = self.target(worker)
        resume_projects, select_projects = self.get_user_incomplete_assignments(worker, projects)
        return render(request, 'workers_hits.html', {'select_projects': select_projects,
                                                     'resume_projects': resume_projects})

    def target(self, worker):
        """
            This function can be extended (e.g., add age/career filters, etc.)
            target worker with user profiles and project settings
        """
        now = datetime.datetime.now()
        projects = Project.objects.filter(Q(complete_indicator=False),
                                          Q(expiry_time__gte=now),
                                          Q(approval_rate__lte=worker.approval_rate) | Q(approval_rate=0))

        # exclude project with no more new HITs and all incomplete HITs are already been done by current worker.
        available_projects = HIT.objects.filter(project__in=projects) \
            .exclude(user_id_list__icontains=worker.id).values('project__id')
        projects = projects.exclude((~Q(id__in=available_projects) & Q(table_complete_indicator=True)))
        return projects

    def get_user_incomplete_assignments(self, worker, projects):
        """
        seperate projects in incomplete_assignments or not.
            1. For projects in incomplete_assignments, show resume button and disable select button
            2. Otherwise, show select button only.
        """
        worker_hits = HIT.objects.filter(Q(project__in=projects), Q(user_id_list__icontains=worker.id))
        now = datetime.datetime.now()
        assignments = Assignment.objects.filter(Q(hit__in=worker_hits), Q(complete_indicator=False),
                                                Q(expiry_time__gte=now))
        print ([a.id for a in assignments])
        if assignments:
            incomplete_project_set = set([i.hit.project for i in assignments])
            incomplete_project = list(incomplete_project_set)
            return incomplete_project, [p for p in projects if p not in incomplete_project_set]
        else:
            return [], projects
