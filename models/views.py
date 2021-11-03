from django.views import generic

from .models import Model, Train

class ModelIndexView(generic.ListView):
    model = Model
    template_name = 'models/index.html'
    context_object_name = 'train_list'
    paginate_by = 10
    ordering = ['-created_at']

class TrainIndexView(generic.ListView):
    model = Train
    template_name = 'train/index.html'
    context_object_name = 'train_list'
    paginate_by = 10
    ordering = ['-created_at']
