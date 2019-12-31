#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# File Name: display_hit_tuples_page.py
"""
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from labeling.models import Project, HIT, Assignment, Table
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import UserProfile
import logging
from django.db.models import Q
import datetime

HIT_EXPIRY_MINUTES = 120

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class DisplayHitTuplesPage(View):
    def get(self, request, *args, **kwargs):
        """ get assignment from assignment table. """
        if 'project_id' in self.kwargs:
            project_id = int(self.kwargs['project_id'])
            project = Project.objects.get(id=project_id)
            samples = Table.objects.filter(project=project)[:5]
        headers = []
        for header in project.csv_header:
            headers.append(header + "_A")
        for header in project.csv_header:
            headers.append(header + "_B")
        return render(request, 'display_hits_tuples.html', {'project': project, 'table': samples, 'headers': headers})

    def post(self, request, *args, **kwargs):
        """
            1. generate a new hit
            2. create a new assignment.
            3. redirect to assignment page.
        """
        user = User.objects.get(username=request.user.username)
        if user:
            worker = UserProfile.objects.get(user=user)
            project_id = request.POST.get('project_id')
            project = Project.objects.get(id=project_id)

            assignment = self.resume_assignment(project, worker)
            if assignment:
                hit = assignment.hit
            else:
                hit = self.generate_hit(project, worker)
                assignment = self.generate_assignment(hit, project, worker)
            if hit.assignment_num == 0 and project.table_complete_indicator:
                project.complete_indicator = True
                project.save()

            return redirect('labeling_service', assignment_id=assignment.id)

    def generate_hit(self, project, worker):
        """ generate a HIT.
             If a HIT(#assign > 0) exist, assign it to current user. Otherwise, generate a new HIT.
         """
        hit = HIT.objects.exclude(user_id_list__icontains=worker.id) \
            .filter(Q(project__id=project.id), Q(assignment_num__gt=0))
        if not hit:
            # generate a new hit
            res = Table.objects.filter(Q(project=project), Q(complete_indicator=False), Q(picked_indicator=False))
            res = res.values('id', 'example')
            if len(res) <= project.HIT_capacity:
                project.table_complete_indicator = True
                project.save()
            res = res[: project.HIT_capacity]
            idx = [i['id'] for i in res]
            # format of examples: id, idA, tupleA1, tupleA2, ..., idB, tupleB1, tupleB2, ...
            examples = [dict({'id': i['id']}, **i) for i in res]
            Table.objects.filter(id__in=idx).update(picked_indicator=True)

            # update HIT table
            hit = HIT(project=project,
                      assignment_num=project.assignment_total,
                      assignment_complete_num=0,
                      label_examples=examples,
                      expiry_time=project.expiry_time
                      )
            hit.save()
            return hit
        else:
            return hit[0]

    def generate_assignment(self, hit, project, worker):
        """ Generate a new Assignment
             Assign HIT to current worker, then update table parameters.
         """
        # add a new line in Assignment
        now = datetime.datetime.now()
        assignment = Assignment(hit=hit, worker=worker,
                                label_examples=hit.label_examples,
                                expiry_time=now + datetime.timedelta(days=60))  # here set expiry days to 60 days.
        # assignment expiry days is not in use right now, need to be modified if you are to use expiry_time for
        # assignments.
        assignment.save()

        # update HIT
        hit.assignment_num -= 1
        hit.user_id_list.append(worker.id)
        hit.assignment_id_list.append(assignment.id)
        hit.save()
        return assignment

    def resume_assignment(self, project, worker):
        """ When users click Resume, do not create a new assignment, retrieval assignents instead."""
        worker_hits = HIT.objects.filter(Q(project=project), Q(user_id_list__icontains=worker.id))
        now = datetime.datetime.now()
        assignments = Assignment.objects.filter(Q(hit__in=worker_hits), Q(complete_indicator=False),
                                                Q(expiry_time__gte=now))
        if assignments:
            return assignments[0]
        else:
            return None
