from enum import Enum

class ParameterTypes(Enum):
    POSITIONAL = 'pos'
    VARIABLE = 'var'
    FLAG = 'flag'

MODEL_PATTERN = '{recipe} {dataset} {model} {source} %s'
NO_MODEL_PATTERN = '{recipe} {dataset} {source} %s'

class PatternBase:
    recipe = 'NaN' # this should be overiden
    command = MODEL_PATTERN # this also should be overiden
    dataset = ParameterTypes.POSITIONAL
    model = ParameterTypes.POSITIONAL
    source = ParameterTypes.POSITIONAL
    loader = ParameterTypes.VARIABLE
    label = ParameterTypes.VARIABLE

    def __init__(self):
        self.parameters = {
            self.process_parameter(var): self.__getattribute__(var)
            for var in self.__dir__() 
            if not var.startswith('__') and not var.endswith('__') and type(self.__getattribute__(var)) == ParameterTypes
        }
        self.parameters.update({'recipe': ParameterTypes.POSITIONAL})
    
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
                if self.parameters[k] == ParameterTypes.VARIABLE and (v and v != ''):
                    extra_params += f' --{k} {v}' # eg. --label TEST,HAHA
                elif self.parameters[k] == ParameterTypes.FLAG and (v and v != ''): # if it's a flag and the value is true or not null
                    extra_params += f' --{k}'

        return self.command.format(**kwargs) %extra_params

COMMAND = {
    'recipe': 'ner.manual',
    'dataset': 'test_ner',
    'source': 'source.json',
    'model': 'blank:id',
    'highlight_chars': 's',
    'label': ['test', 'test2']
}

class NER_MANUAL(PatternBase):
    recipe = 'ner.manual'
    patterns = ParameterTypes.VARIABLE
    exclude = ParameterTypes.VARIABLE
    highlight_chars = ParameterTypes.FLAG

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

class TRAIN(PatternBase):
    recipe = 'train'
    output_dir = ParameterTypes.POSITIONAL

    ner = ParameterTypes.FLAG
    textcat = ParameterTypes.FLAG
    textcat_multilabel = ParameterTypes.FLAG
    database = ParameterTypes.POSITIONAL # flag before positional

    base_model = ParameterTypes.VARIABLE
    eval_split = ParameterTypes.VARIABLE
    lang = ParameterTypes.VARIABLE
    gpu_id = ParameterTypes.VARIABLE

    label_stats = ParameterTypes.FLAG
    verbose = ParameterTypes.FLAG
    silent = ParameterTypes.FLAG
    


RECIPE_PATTERNS = {
    'ner.manual': NER_MANUAL(),
    'ner.correct': NER_CORRECT(),
    'ner.teach': NER_TEACH(),
    'train': TRAIN()
    # 'ner.teach': MODEL_PATTERN %('ner.teach'),
    # 'textcat.manual': NO_MODEL_PATTERN %('textcat.manual'),
    # 'textcat.correct': MODEL_PATTERN %('textcat.correct'),
    # 'textcat.teach': MODEL_PATTERN %('textcat.teach')
}

RESERVED_FIELDS = ['recipe', 'dataset', 'source']

def get_command(recipe, **kwargs):
    """Given a recipe and parameters, generate the prodigy command"""
    return RECIPE_PATTERNS[recipe](recipe=recipe, **kwargs)

