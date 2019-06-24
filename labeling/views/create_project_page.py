#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# File Name: create_projet_page.py
"""
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from labeling.models import Project, Table
from labeling.forms import CreateProjectForm, UploadDatasetForm
from labeling.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging, datetime, csv

logger = logging.getLogger(__name__)
AGE_CHOICES = ((0, ''),
        (1, 'under 10'),
        (2, '11 to 20'),
        (3, '21 to 30'),
        (4, '31 to 40'),
        (5, 'above 41'))
GENDER_CHOICES = ((0, ''), (1, 'female'), (2, 'male'))
approval_hit_count_choices = ((6, 6),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5))
expiry_days_count = ((6, 6),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5))
# approval_rate = ((0.25, 0.25), (0.5, 0.5), (0.75, 0.75))

@method_decorator(login_required, name='dispatch')
class CreateProjectPage(View):
    def get(self, request, *args, **kwargs):
        form  = CreateProjectForm(gender_choices = GENDER_CHOICES,age = AGE_CHOICES,
                approval_hit_count_choices = approval_hit_count_choices,
                expiry_days_count= expiry_days_count)
        upload_file_form = UploadDatasetForm()
        return render(request, 'create_project.html', {'create_form': form, 'upload_file_form': upload_file_form })

    def post(self, request, *args, **kwargs):
        """
            load parameters of create-project-form into db, and create a project in the database.
        """
        username = request.user.username
        user = User.objects.get(username=username)
        if user:
            owner = UserProfile.objects.get(user = user)
        name = request.POST.get('project_name')
        descriptions = request.POST.get('description')
        HIT_capacity = request.POST.get('tuples_count')
        assignment_total = request.POST.get('worker_count')
        uploaded_file = request.FILES.get('docfile')

        # rescale approval rate into [0,1]
        approval_rate = 0
        if request.POST.get('approval_rate'):
            approval_rate = float(request.POST.get('approval_rate')) / 100

        # transfer days count into expiry time.
        expiry_days_count = 0
        if request.POST.get('expiry_days_count'):
            expiry_days_count = int(request.POST.get('expiry_days_count'))
        now = datetime.datetime.now()
        expiry_time = now + datetime.timedelta(days = int(expiry_days_count))

        if not uploaded_file:
            return redirect('project_actions', success=0)

        project = Project(name = name,owner = owner,descriptions = descriptions,
                HIT_capacity= HIT_capacity,  assignment_total = assignment_total,
                expiry_time = expiry_time, uploaded_file = uploaded_file, approval_rate = approval_rate)
        project.save()

        if self.save_uploaded_file(project):
            return redirect('project_actions', success = 1)
        else:
            return redirect('project_actions', success=0)

    def save_uploaded_file(self, project):
        """
            save uploaded file into database.
            csv header is [idA, tupleA1, tupleA2, ..., idB, tupleB1, tupleB2, ..]
            example header: id, name, address, id, name, address
            @param project[Project]: load csv file of a project into Table db.
            @rapram [boolean]: return True if loading file successfully, return False otherwise.
        """
        ufile = project.uploaded_file
        if not ufile:
            return False
        fin = ufile.read().splitlines()
        dr = [i for i in csv.reader(fin)]
        if not dr:
            return False
        project.csv_header = [dr[0][i] for i in range(len(dr[0])) if i < len(dr[0]) / 2]
        project.save()
        # to seperate matching pairs, add _A to header of the first pair, add _B to header of the second pair.
        new_csv_header = [dr[0][i] + '_A' if i < len(dr[0]) / 2 else dr[0][i] + '_B' for i in range(len(dr[0]))]

        to_db = [Table(project = project,
            example = [{new_csv_header[j]:i[j] for j in range(len(new_csv_header))}]) for i in dr[1:]]
        Table.objects.bulk_create(to_db)
        return True
