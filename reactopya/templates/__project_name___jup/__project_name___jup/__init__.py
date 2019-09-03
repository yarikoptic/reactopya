####################################################################
## This file is automatically generated
## Do not edit manually
####################################################################

from .all_widgets import *
{% for X in additional_jupyter_imports %}
{{ X }}
{% endfor %}

from ._version import __version__
from .init import init_jupyter, init_colab

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': '{{ project_name }}_jup',
        'require': '{{ project_name }}_jup/extension'
    }]

