from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.views import generic
from django.conf import settings
from django import forms
from djproxy.views import HttpProxy
from rest_framework import serializers, viewsets
from django.utils.safestring import mark_safe

from .patterns import RECIPE_PATTERNS, ParameterTypes, RESERVED_FIELDS
from .models import Session
from .serializers import SessionSerializer

class ProxyView(HttpProxy):
    base_url = 'http://localhost:'

    @property
    def proxy_url(self):
        """Return URL to the resource to proxy."""
        return self.base_url + self.kwargs.get('url', '')

class SessionViewSet(viewsets.ViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class IndexView(generic.ListView):
    model = Session
    template_name = 'sessions/index.html'
    context_object_name = 'session_list'
    paginate_by = 10
    ordering = ['-created_at']

class DetailView(generic.DetailView):
    model = Session
    template_name = 'sessions/detail.html'

def prodigy_redirect(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.status != 'Active':
        return HttpResponseNotFound('Session is offline')

    url = settings.SESSION_URL_BASE + str(session.port) + '/'
    return redirect(url)

class SessionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('options') is not None:
            self.options = kwargs.pop('options')
        self.recipe_value = kwargs.pop('recipe')

        super(SessionForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.label is not None:
                field.widget.attrs = {
                    'class': 'form-control',
                    'id': field.label.lower()
                }
            
            if name == 'recipe':
                field.disabled = True
                field.initial = self.recipe_value
        
        if self.options is not None:
            for i, (name, param) in enumerate(self.options.parameters.items()):
                if name in RESERVED_FIELDS:
                    continue

                field = param.generate_field()
                self.fields[name] = field
    
    def get_options(self):
        options = {}
        for name, v in self.cleaned_data.items():
            if name not in RESERVED_FIELDS and self.options.parameters.get(name) is not None:
                options[name] = self.options.parameters[name].clean(v)
        return options

    class Meta:
        fields = ('name', 'recipe', 'dataset') 
        model = Session

def create_session(request, recipe):
    recipe_pattern = RECIPE_PATTERNS[recipe]

    form = SessionForm(request.POST or None, recipe=recipe, options=recipe_pattern)
    if form.is_valid():
        meta = form.get_options()
        session = Session(name=form.cleaned_data['name'], recipe=form.cleaned_data['recipe'], dataset=form.cleaned_data['dataset'], meta=meta)
        session.save()
        return redirect('tasks:detail', pk=session.id)

    return render(request, "sessions/create_recipe.html", {'form': form})

class RecipeForm(forms.Form):
    recipe = forms.ChoiceField(label='recipe', choices=list(zip(RECIPE_PATTERNS.keys(), RECIPE_PATTERNS.keys())))

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['recipe'].widget.attrs = {'class': 'form-control'}

def get_recipe(request):
    recipes = list(RECIPE_PATTERNS.keys())
    if request.method == 'POST':
        recipe = request.POST.get('recipe')
        if recipe:
            return HttpResponseRedirect(f'/sessions/new/{recipe}') # redirect to like /sessions/new/ner.manual
        else:
            return render(request, 'sessions/create.html', {'recipes': recipes, 'error_message': 'Select a recipe'})
    else:
        return render(request, 'sessions/create.html', {'recipes': recipes})

def start_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.active:
        # not allowed
        return HttpResponseForbidden('session is already active')
    
    session.setup_prodigy_session()
    return redirect('tasks:detail', pk=session_id)

def stop_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if session.disabled:
        # not allowed
        return HttpResponseForbidden('session is not active')
    
    session.close()
    return redirect('tasks:detail', pk=session_id)
