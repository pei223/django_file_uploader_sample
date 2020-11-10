import logging
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger("default")


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "index.html", {})
