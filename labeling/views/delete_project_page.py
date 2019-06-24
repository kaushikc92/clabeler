#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# File Name: delete_project_page.py
"""
from django.views.generic import View
from django.shortcuts import render
from labeling.models import Project
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from labeling.models import UserProfile

import logging

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class DeleteProjectPage(View):
    def post(self, request, *args, **kwargs):
        """ delete a project from database and redirect to owner-project page """
        project_id = self.kwargs.get('delete_project_id', None)
        if project_id:
            project = Project.objects.get(id = int(project_id))
            if project:
                project.delete()
        username = request.user.username
        user = User.objects.get(username=username)
        if user:
            owner = UserProfile.objects.get(user = user)

        projects = Project.objects.filter(owner = owner).exclude(id = int(project_id))
        return render(request, 'project_actions.html', {'projects': projects})

