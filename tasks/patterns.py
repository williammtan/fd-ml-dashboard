from enum import Enum
from django import forms
from django.utils.safestring import mark_safe
import os

from models.models import Model

class ParameterTypes(Enum):
    POSITIONAL = 'pos'
    VARIABLE = 'var'
    FLAG = 'flag'

class Parameter:
    def __init__(self, type, default=None, help='', required=False):
        self.type = type
        self.default = default
        self.help = help
        if self.type == ParameterTypes.POSITIONAL: # always required if the parameter is positional
            self.required = True
        else:
            self.required = required
    
    def generate_field(self):
        """Return a django Form Field"""
        help_text = mark_safe(f'<a class="helptext">?<span>{self.help}</span></a>')

        if self.type == ParameterTypes.FLAG:
            field = forms.BooleanField(required=False, help_text=help_text, initial=self.default)
        elif self.type == ParameterTypes.VARIABLE:
            field = forms.CharField(required=False or self.required, help_text=help_text, initial=self.default)
        elif self.type == ParameterTypes.POSITIONAL:
            field = forms.CharField(required=True, help_text=help_text, initial=self.default)

        return field
    
    def clean(self, data):
        """Clean output from cleaned_data"""
        return None if data == '' else data

class ModelParameter(Parameter):
    def __init__(self, model, type, default=None, help='', required=False):
        self.model = model
        super().__init__(type=type, default=default, help=help, required=required)
    
    def generate_field(self):
        choices = [(m.id, str(m)) for m in self.model.objects.all()]
        field = forms.ChoiceField(choices=choices)
        return field
    
    def clean(self, id):
        """Clean output from cleaned_data"""
        return os.path.join(self.model.objects.get(pk=id).file_path, 'model-best')


MODEL_PATTERN = '{recipe} {dataset} {model} {source} %s'
NO_MODEL_PATTERN = '{recipe} {dataset} {source} %s'

class PatternBase:
    recipe = 'NaN' # this should be overiden
    command = MODEL_PATTERN # this also should be overiden
    dataset = Parameter(ParameterTypes.POSITIONAL, help='Prodigy dataset to save annotations to.')
    label = Parameter(ParameterTypes.VARIABLE, help='Comma-separated list of labels to annotate (eg. MYLABEL,MYOTHERLABEL)', required=True)
    model = ModelParameter(Model, ParameterTypes.POSITIONAL, default='blank:id', help='Loadable spaCy pipeline for tokenization or blank:lang for a blank model (e.g. blank:id for Indonesian).', required=True)
    source = Parameter(ParameterTypes.POSITIONAL, help='Path to text source or - to read from standard input.')
    loader = Parameter(ParameterTypes.VARIABLE, help='Optional ID of text source loader. If not set, source file extension is used to determine loader.')

    def __init__(self):
        self.parameters = {
            self.process_parameter(var): self.__getattribute__(var)
            for var in self.__dir__() 
            if not var.startswith('__') and not var.endswith('__') 
            and (type(self.__getattribute__(var)) == Parameter or issubclass(type(self.__getattribute__(var)), Parameter))
            and type(self.__getattribute__(var).type) == ParameterTypes
        }
        self.parameters.update({'recipe': Parameter(ParameterTypes.POSITIONAL, help='Prodigy recipe')})
    
    def process_parameter(self, text):
        return text.replace('_', '-')
    
    def __call__(self, **kwargs):
        kwargs = {self.process_parameter(k): v for k,v in kwargs.items()}

        extra_params = ''
        for k,v in kwargs.items():
            if type(v) != str:
                try: # check if iterable if not a string
                    _ = (e for e in v)
                    v = ','.join(v)
                except TypeError:
                    pass

            if k in self.parameters:
                if self.parameters[k].type == ParameterTypes.VARIABLE and (v and v != ''):
                    extra_params += f' --{k} {v}' # eg. --label TEST,HAHA
                elif self.parameters[k].type == ParameterTypes.FLAG and (v and v != ''): # if it's a flag and the value is true or not null
                    extra_params += f' --{k}'

        return self.command.format(**kwargs) %extra_params

class NER_MANUAL(PatternBase):
    recipe = 'ner.manual'
    model = Parameter(ParameterTypes.POSITIONAL, default='blank:id', help='Loadable spaCy pipeline for tokenization or blank:lang for a blank model (e.g. blank:id for Indonesian).', required=True)
    patterns = Parameter(ParameterTypes.VARIABLE, help='Optional path to match patterns file to pre-highlight entity spans.')
    exclude = Parameter(ParameterTypes.VARIABLE, help='Comma-separated list of dataset IDs containing annotations to exclude.')
    highlight_chars = Parameter(ParameterTypes.FLAG, help=' Allow highlighting individual characters instead of snapping to token boundaries. If set, no "tokens" information will be saved with the example.')

class NER_CORRECT(PatternBase):
    recipe = 'ner.manual'
    update = ParameterTypes.FLAG
    unsegmented = ParameterTypes.FLAG
    component = ParameterTypes.VARIABLE

class NER_TEACH(PatternBase):
    recipe = 'ner.teach'
    patterns = ParameterTypes.VARIABLE
    exclude = ParameterTypes.VARIABLE
    unsegmented = ParameterTypes.FLAG


RECIPE_PATTERNS = {
    'ner.manual': NER_MANUAL(),
    'ner.correct': NER_CORRECT(),
    'ner.teach': NER_TEACH()
}

RESERVED_FIELDS = ['recipe', 'dataset', 'source']

def get_command(recipe, **kwargs):
    """Given a recipe and parameters, generate the prodigy command"""
    return RECIPE_PATTERNS[recipe](recipe=recipe, **kwargs)

