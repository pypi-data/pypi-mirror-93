from django import forms


class htmxSelect(forms.Widget):
    template_name = "mirforms/widgets/htmx_select/htmx_select.html"
    option_template_name = "mirforms/widgets/htmx_select/htmx_select_option.html"

    def __init__(
        self,
        url,
        select_data,
        queryset,
        htmx_attrs=None,
        option_template_name=None,
        attrs=None,
    ):
        super().__init__(attrs=attrs)
        self.select_data = select_data
        self.queryset = queryset
        self.url = url
        self.htmx_attrs = htmx_attrs
        self.option_template_name = (
            option_template_name or self.option_template_name
        )

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context["select_url"] = self.select_data
        context["option_template_name"] = self.option_template_name
        context["url"] = self.url
        context["htmx_attrs"] = self.htmx_attrs
        context["queryset"] = self.queryset[:10]
        context["widget_name"] = self.queryset.model.__name__

        try:
            value = context.get("widget").get("value", "")
            txt = self.queryset.get(uuid=value).designation
            context["value"] = value
            context["txt"] = txt
        except:
            pass
        return context
