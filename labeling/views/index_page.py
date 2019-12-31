from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class IndexPage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
