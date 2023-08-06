import json
import urllib.parse
from django import forms
from mirforms.utils import encode
from mirforms.widgets import htmxSelect
from django.urls import reverse_lazy


class BooleanField(forms.BooleanField):
    def __init__(self, is_inline=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_inline = is_inline


class HtmxChoiceField(forms.Field):
    def __init__(self, hselect_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Encode params to be sent over URL
        select_data = encode(
            json.dumps(
                {
                    "module": hselect_class.__module__,
                    "klass": hselect_class.__class__.__name__,
                }
            )
        )
        self.widget = htmxSelect(
            url=reverse_lazy("mirforms:select_inlines"),
            select_data=urllib.parse.quote_plus(select_data),
            queryset=hselect_class.get_queryset(),
            htmx_attrs=hselect_class.htmx_attrs,
        )
