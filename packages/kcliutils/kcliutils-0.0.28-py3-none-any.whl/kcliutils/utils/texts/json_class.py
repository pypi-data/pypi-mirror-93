# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Dict
import string

# Local
from .core_texts import json_class
from .utils import comment_line, multi_replace

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def new_json_class(class_name: str, d: Dict[str, any]) -> str:
    return multi_replace(
        json_class,
        {
            '[CLASS_NAME]': class_name,
            '[CLASS_NAME_COMMENT_LINE]': comment_line('class: {}'.format(class_name)),
            '[INIT_VARS]': __init_vars_str(d)
        }
    )


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __init_vars_str(
    d: Dict[str, any],
    indent_spaces: int = 4
) -> str:
    init_str = ''

    for k in d.keys():
        formatted_key = __formatted_key(k)

        init_str += '{}self.{} = d.get(\'{}\')'.format(
            ' ' * 2 * indent_spaces,
            formatted_key,
            k
        )

    return init_str

def __formatted_key(s: str) -> str:
    _s = ''

    for i, c in enumerate(s):
        if c in string.punctuation:
            c = '_'
        elif c in string.ascii_uppercase:
            c = '{}{}'.format('_' if i > 0 else '', c.lower())

        _s += c

    return _s


# ---------------------------------------------------------------------------------------------------------------------------------------- #