from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from labeling.models import Assignment

import logging
import json
import pdb

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class CompletionNoticePage(View):
    def get(self, request, *args, **kwargs):
        assignment_id = self.kwargs.get('assignment_id', None)
        assignment = Assignment.objects.get(pk=assignment_id)
        headers = assignment.hit.project.csv_header
        lallrows, rallrows, labels_and_ids = self.get_rows_and_counts(assignment.label_examples, headers)
        print(labels_and_ids)
        return render(request, 'completion_notice.html',
                      {'fields': lallrows, 'headers': headers, 'lrows': lallrows, 'rrows': rallrows,
                       'labels': labels_and_ids, 'assignment_id': assignment_id})

    def get_rows_and_counts(self, label_examples, headers):
        lrows = []
        rrows = []
        labels_and_ids = []
        for example in label_examples:
            label_id = example.get('label')
            labels_and_ids.append(label_id)
            rowA = []
            rowB = []
            for header in headers:
                rowA.append(example['example'][0][header + "_A"])
                rowB.append(example['example'][0][header + "_B"])

            lrows.append(rowA)
            rrows.append(rowB)

        return lrows, rrows, labels_and_ids

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        assignment_id = request.POST.get('assignment_id', None)
        print 'ass: ', assignment_id
        assignment = Assignment.objects.get(pk=assignment_id)
        label_examples = assignment.label_examples
        for index, ex in enumerate(label_examples):
            ex['label'] = request.POST.get(str(index + 1))
        assignment.save()
        return render(request, 'review_labelling.html')
