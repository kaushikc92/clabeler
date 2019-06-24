from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import Assignment
from collections import Counter

import logging
import simplejson
import json
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class LabelingServicePage(View):

    labels = [
        {
            "name": "Yes", "value": "t"
        },
        {
            "name": "No", "value": "f"
        },
        {
            "name": "Unsure", "value": "u"
        },
        {
            "name": "Add comment", "value": "c"
        },
        {
            "name": "Show Entire Tuple Pair", "value": "s"
        },
        {
            "name": "Add Tag", "value": "m"
        },

    ]

    def get(self, request, *args, **kwargs):
        assignment_id = self.kwargs['assignment_id']
        num_pairs = int(self.kwargs.get('num_pairs', 1))
        owner = request.user.username
        save_flag = request.GET.get('save_flag', None)
        reload_flag = request.GET.get('reload', None)

        assignment = Assignment.objects.get(pk=assignment_id)

        return_data = {}
        return_data['next_url'] = 'labeling_service'
        return_data['assignment_id'] = assignment_id
        return_data['panel_label'] = 'Label tuple pairs'
        return_data['labels'] = self.labels
        return_data['labeling_completed'] = False
        return_data['headers'] = [assignment.hit.project.csv_header]
        ids, rows, counts = self.get_rows_and_counts(assignment.label_examples, assignment.hit.project.csv_header)
        # Trying to access a completed assignment redirects to hits page
        if len(ids) == 0:
            return redirect('completion_notice')

        return_data['ids'] = ids
        return_data['pair_id'] = ids[0]
        return_data['rows'] = rows
        return_data['true_label_count'] = counts['true_label_count']
        return_data['false_label_count'] = counts['false_label_count']
        return_data['unsure_label_count'] = counts['unsure_label_count']
        return_data['done_count'] = counts['done_count']
        return_data['total_count'] = counts['total_count']

        return_data = simplejson.loads(simplejson.dumps(return_data, ignore_nan=True))
        logger.info('labeling_service_page view return data: {0}'.format(return_data))
        if reload_flag == "false":
            return HttpResponse(json.dumps(return_data), content_type="application/json")
        else:
            return render(request, 'label_tuple_pairs.html', return_data)

    def get_rows_and_counts(self, label_examples, headers):
        counts = {
            'true_label_count': 0,
            'false_label_count': 0,
            'unsure_label_count': 0,
            'done_count': 0,
            'total_count': 0
        }

        rows = []
        ids = []
        done = False

        for example in label_examples:
            counts['total_count'] = counts['total_count'] + 1
            label = example.get('label', None)
            if label:
                counts['done_count'] = counts['done_count'] + 1
                if label == 't':
                    counts['true_label_count'] = counts['true_label_count'] + 1
                elif label == 'f':
                    counts['false_label_count'] = counts['false_label_count'] + 1
                if label == 'u':
                    counts['unsure_label_count'] = counts['unsure_label_count'] + 1
            else:
                if not done:
                    rowA = []
                    rowB = []
                    for header in headers:
                        rowA.append(example['example'][0][header + "_A"])
                        rowB.append(example['example'][0][header + "_B"])
                    rows = [[rowA], [rowB]]
                    ids.append(example['id'])
                    done = True

        return ids, rows, counts

    def post(self, request, *args, **kwargs):
        assignment_id = self.kwargs['assignment_id']
        pair_id = int(self.request.POST['pair_id'])
        label = self.request.POST['label']
        # num_pairs = int(self.kwargs['num_pairs'])
        owner = request.user.username
        save_flag = request.POST.get('save_flag', None)
        assignment = Assignment.objects.get(pk=assignment_id)

        if save_flag:
            self.save_label_to_assignment(assignment, pair_id, label)

        ids, rows, counts = self.get_rows_and_counts(assignment.label_examples, assignment.hit.project.csv_header)

        response = {}

        if len(rows) == 0:
            self.save_assignment(assignment)

        response['label_complete'] = (len(rows) == 0)

        if save_flag:
            return HttpResponse(json.dumps(response), content_type="application/json")

        # return redirect('labeling_service', project_id, wf_id, ds_name, num_pairs)

    def save_label_to_assignment(self, assignment, pair_id, label):
        label_examples = assignment.label_examples
        new_label_examples = []
        for example in label_examples:
            if(example['id'] == pair_id):
                print ("here")
                example['label'] = label
            new_label_examples.append(example)

        assignment.label_examples = new_label_examples
        assignment.save()

    def save_assignment(self, assignment):
        """
            update db when an assignment is submit. add by Jennifer.
            1. update assignment
            2. update hits
        """
        assignment.complete_indicator = True
        assignment.save()
        hit = assignment.hit
        project = hit.project
        assignment_complete_num = hit.assignment_complete_num + 1
        hit.assignment_complete_num = assignment_complete_num
        hit.save()
        if assignment_complete_num == project.assignment_total:
            assignment_id_list = hit.assignment_id_list
            assignments = [Assignment.objects.get(id = i) for i in assignment_id_list]
            hit_examples = self.major_vote(assignments, hit.label_examples)
            hit.label_examples = hit_examples
            hit.save()

    def major_vote(self, assignments, examples):
        """ currently we only implement the major vote mode. add by Jennifer """
        hit_examples = []
        for example in examples:
            idx = example["id"]
            idx_labels = [k["label"] for i in assignments for k in i.label_examples if k["id"] == idx]
            c = Counter(idx_labels)
            label = c.most_common()[0][0]
            hit_examples.append(dict({"label": label}, **example))
        return hit_examples
