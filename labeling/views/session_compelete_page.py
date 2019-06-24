from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.models import User
from labeling.models import Project, HIT, Assignment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import UserProfile
import logging
import pdb
from django.db.models import Q
import csv

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class SessionCompletePage(View):

    def get(self, request, *args, **kwargs):
        username = request.user.username
        user = User.objects.get(username=username)
        if user:
            owner = UserProfile.objects.get(user = user)
            projects = Project.objects.filter(owner=owner)
            return render(request, 'session_complete.html')
       

    # def get(self, request, *args, **kwargs):
    #     username = request.user.username
    #     user = User.objects.get(username=username)
    #     pdb.set_trace()
    #     if user:
    #         owner = UserProfile.objects.get(user = user)
    #         hits = Project.objects.filter(owner=owner)
    #         ass_id = int(self.kwargs['assignment_id'])
    #         res = Assignment.objects.get(id = ass_id)
    #         return render(request, 'display_hits_tuples.html', {'assignment': res })

    # def post(self, request, *args, **kwargs):
    #     user = User.objects.get(username = request.user.username)
    #     # pdb.set_trace()
        
    #     if user:
    #         worker = UserProfile.objects.get(user=user)
    #     # else:
    #     #     html = "<html><body>Please return to create user account. </html>"
    #     #     return HttpResponse(html)

    #     # TODO: how to get project_id and table?
    #     project_id = request.POST.get('project_id')
    #     project = Project.objects.get(id = project_id)
    #     filename = str(project.uploaded_file.file.name)

    #     hit = self.generate_hit(project, worker, filename)
    #     # if not hit:
    #     #     html = "<html><body>Table is already done. </html>"
    #     #     return HttpResponse(html)
    #     assignment = self.generate_assignment(hit, project, worker)
    #     if hit.assignment_num == 0 and project.table_complete_indicator:
    #         project.update(complete_indicator = True)
    #     return redirect('display_hit_tuples', assignment_id = assignment.id)


    # def generate_hit(self, project, worker, filename):
    #     """ generate a HIT.
    #         If a HIT(#assign > 0) exist, assign it to current user. Otherwise, generate a new HIT.
    #     """
    #     hit = HIT.objects.filter(Q(project__id = project.id), Q(assignment_num__gt = 0))
    #     if not hit:
    #         # generate a new hit
    #         with open(filename,'r') as fin:
    #             dr = csv.DictReader(fin)
    #             # pdb.set_trace()
    #             if not dr:
    #                 logging.warn('table is Done, exit') # TODO: table Done, move it to targeting page(worker HIT display page.)
    #                 return hit
    #             headers = dr.fieldnames
    #             # pdb.set_trace()
    #             res = [[i['tuple_id'], i['tuple_content']] if k < project.HIT_capacity else i for k, i in enumerate(dr)]
    #             hit_capacity = min(project.HIT_capacity, len(res))
    #             examples = res[: hit_capacity]
    #             datas = res[hit_capacity: ]
    #         if not datas:
    #             project.update(table_complete_indicator = True)
    #         with open(filename, 'w') as fout:
    #             writer = csv.DictWriter(fout, headers)
    #             writer.writeheader()
    #             writer.writerows(datas)

    #         # update HIT table
    #         hit = HIT(project = project,
    #                 assignment_num = project.assignment_total,
    #                 assignment_complete_num = 0,
    #                 label_examples = examples,
    #                 assignment_id_list = list,
    #                 user_id_list = list,
    #                 expiry_time = project.expiry_time
    #                 )
    #         hit.save()
    #         return hit
    #     else:
    #         return hit[0]

    # def generate_assignment(self, hit, project, worker):
    #     """ Generate a new Assignment
    #         Assign HIT to current worker, then update table parameters.
    #     """
    #     assignment_num = hit.assignment_num - 1
    #     user_id_list = hit.user_id_list
    #     user_id_list.append(worker.id)
    #     assignment_id_list = hit.assignment_id_list

    #     # add a new line in Assignment
    #     now = datetime.datetime.now()
    #     assignment = Assignment(HIT = hit, worker = worker,
    #             label_examples = hit.label_examples,
    #             expiry_time = now + datetime.timedelta(minutes = HIT_EXPIRY_MINUTES))
    #     assignment.save()

    #     # update HIT
    #     assignment_id_list.append(assignment.id)
    #     hit.update(assignment_num = assignment_num,
    #             user_id_list = user_id_list,
    #             assignment_id_list = assignment_id_list)
    #     hit.save()
    #     return assignment
        