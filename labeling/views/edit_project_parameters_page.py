#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# File Name: edit_project_parameters_page.py
"""
from django.views.generic import View
from django.shortcuts import render, redirect
from labeling.models import Project
from labeling.forms import EditProjectParametersForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging, datetime


logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class EditProjectParametersPage(View):
    def get(self, request, *args, **kwargs):
        # project_id = self.kwargs['project_id']
        edit_form  = EditProjectParametersForm()
        return render(request, 'edit_project_parameters.html', {'edit_form': edit_form})

    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['project_id']
        project = Project.objects.get(id = project_id)

        self.update_project(project,
                name = request.POST.get('project_name', None),
                descriptions = request.POST.get('description', None),
                HIT_capacity = request.POST.get('tuples_count', None),
                assignment_total = request.POST.get('worker_count', None),
                approval_rate = request.POST.get('approval_rate', None),
                expiry_days_count = request.POST.get('expiry_days_count', None))
        project.save()
        return redirect('project_actions')

    def update_project(self, project, **parameters):
        """ update parameters of project """
        if not project:
            return False
        for k, v in parameters.items():
            if not v:
                continue
            if k == 'expiry_days_count':
                project.expiry_time = project.created_at + \
                    datetime.timedelta(days = int(v))
            project.name = v if k is 'name' else project.name
            project.descriptions = v if k is 'descriptions' else project.descriptions
            project.HIT_capacity = v if k is 'HIT_capacity' else project.HIT_capacity
            project.assignment_total = v if k is 'assignment_total' else project.assignment_total
            project.approval_rate = float(v) / 100 if k is 'approval_rate' else project.approval_rate
        return True
