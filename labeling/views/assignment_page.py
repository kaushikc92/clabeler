#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Jennifer Cao
# Email: jennifer.cao@wisc.edu
# Created Time : Mon Apr 15 12:57:07 2019
# File Name: assignment_page.py
"""
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import HIT, Assignment, Project, UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
import csv, datetime
from collections import Counter

import logging
logger = logging.getLogger(__name__)
HIT_EXPIRY_MINUTES = 120


@method_decorator(login_required, name='dispatch')
class AssignmentPage(View):
    def get(self, request, *args, **kwargs):
        """
            1. worker select a HIT.
            2. generate a HIT from CSV file.
            3. display questions of this HIT.
        """
        user = User.objects.get(username = request.user.username)
        if user:
            worker = UserProfile.objects.get(user=user)
        else:
            html = "<html><body>Please return to create user account. </html>"
            return HttpResponse(html)

        # TODO: how to get project_id and table?
        project_id = request.GET.get('project_id')
        project = Project.objects.get(id = project_id)
        filename = project.uploaded_file

        hit = self.generate_hit(project, worker, filename)
        if not hit:
            html = "<html><body>Table is already done. </html>"
            return HttpResponse(html)
        assignment = self.generate_assignment(hit, project, worker)
        if hit.assignment_num == 0 and project.table_complete_indicator:
            project.update(complete_indicator = True)
        return render(request, 'XXX.html', {'assignment': assignment, 'hit': hit})

    def generate_hit(self, project, worker, filename):
        """ generate a HIT.
            If a HIT(#assign > 0) exist, assign it to current user. Otherwise, generate a new HIT.
        """
        hits = HIT.objects.exclude(user_id_list__icontains = worker.id)\
                .filter(Q(project__id = project.id), Q(assignment_num__gt = 0))
        if not hits:
            # generate a new hit
            with open(filename,'r') as fin:
                dr = csv.DictReader(fin)
                if not dr:
                    logging.warn('table is Done, exit') # TODO: table Done, move it to targeting page(worker HIT display page.)
                    return False
                headers = dr.fieldnames
                res = [[i['tuple_id'], i['tuple_content']] if k < project.HIT_capacity else i for k, i in enumerate(dr)]
                hit_capacity = min(project.HIT_capacity, len(res))
                examples = res[: hit_capacity]
                datas = res[hit_capacity: ]
            if not datas:
                project.update(table_complete_indicator = True)
            with open(filename, 'w') as fout:
                writer = csv.DictWriter(fout, headers)
                writer.writeheader()
                writer.writerows(datas)

            # update HIT table
            hit = HIT(project = project,
                    assignment_num = project.assignment_total,
                    assignment_complete_num = 0,
                    label_examples = examples,
                    assignment_id_list = list,
                    user_id_list = list,
                    expiry_time = project.expiry_time
                    )
            hit.save()
            return hit
        return hits[0]

    def generate_assignment(self, hit, project, worker):
        """ Generate a new Assignment
            Assign HIT to current worker, then update table parameters.
        """
        assignment_num = hit.assignment_num - 1
        user_id_list = hit.user_id_list
        user_id_list.append(worker.id)
        assignment_id_list = hit.assignment_id_list

        # add a new line in Assignment
        now = datetime.datetime.now()
        assignment = Assignment(HIT = hit, worker = worker,
                label_examples = hit.label_examples,
                expiry_time = now + datetime.timedelta(minutes = HIT_EXPIRY_MINUTES))
        assignment.save()

        # update HIT
        assignment_id_list.append(assignment.id)
        hit.update(assignment_num = assignment_num,
                user_id_list = user_id_list,
                assignment_id_list = assignment_id_list)
        hit.save()
        return assignment

    def post(self, request, *args, **kwargs):
        """ Collect user's actions. """
        #form = WorkerSelectHITForm(request.POST)
        # TODO: pls put form here.
        form = None
        success = False
        if form.is_valid():
            # TODO: how to get assignment from request?
            assignment = Assignment.objects.get(id = request.POST['assignment_id'])
            now = datetime.datetime.now()
            success = True
            if request.POST['submit'] is True:
                success = self.save(request.POST['labels'], assignment) # TODO: how to get labels from POST page?
            if request.POST['cancel'] == True or now > assignment.expiry_time: # TODO: how to find if it is expired?
                success = self.destroy(assignment)
        return render(request, 'XXXX.html', {'form': form, 'success': success})

    def save(self, labels, assignment):
        """
            update db when an assignment is submit.
            1. update assignment
            2. update hits
        """
        examples = assignment.label_examples
        label_examples = [examples + [labels[i[0]]] if i[0] in labels else False for i in examples]
        if False not in label_examples:
            assignment.update(label_examples = label_examples, complete_indicator = True)
            hit = assignment.hit
            project = hit.project
            assignment_complete_num = hit.assignment_complete_num - 1
            hit.update(assignment_complete_num = assignment_complete_num)
            if assignment_complete_num == project.assignment_total:
                assignment_id_list = hit.assignment_id_list
                assignments = [Assignment.objects.get(id = i) for i in assignment_id_list]
                hit_examples = self.major_vote(assignments, examples)
                hit.update(label_examples = hit_examples)
            return True
        else:
            return False

    def destroy(self, assignment):
        """
            update db when an assignment is canceled or expired.
            1. update hit: assignment_complete_num, user_id_list, assignment_id_list
            2. update project: complete_indicator
            3. update assignment: delete
        """
        hit = assignment.hit
        project = hit.project
        assignment_num = hit.assignment_num + 1
        assignment_id = assignment.id
        worker_id = assignment.worker.id
        user_id_list = [i for i in hit.user_id_list if i != worker_id]
        assignment_id_list = [i for i in hit.assignment_id_list if i != assignment_id]
        hit.update(user_id_list = user_id_list, assignment_id_list = assignment_id_list, assignment_num = assignment_num)
        if project.complete_indicator:
            project.update(complete_indicator = False)
        assignment.delete()
        return True

    def major_vote(self, assignments, examples):
        """ currently we only implement the major vote mode. """
        examples = [example + [''] for example in examples]
        hit_examples = []
        for example in examples:
            idx = example[0]
            idx_labels = [k[-1] for i in assignments for k in i.label_examples if k[0] == idx]
            c = Counter(idx_labels)
            label = c.most_common()[0][0]
            hit_examples.append(example + [label])
        return hit_examples
