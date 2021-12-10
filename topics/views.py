from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Count

from .models import Topic

class IndexView(ListView):
    model = Topic
    paginate_by = 10
    template_name = "topics/index.html"
    
    def get_queryset(self):
        return Topic.objects.annotate(p_count=Count('producttopic')).order_by('-p_count')

class UpdateView(UpdateView):
    model = Topic
    fields = ['renamed', 'is_deleted']
    template_name = "topics/update.html"
