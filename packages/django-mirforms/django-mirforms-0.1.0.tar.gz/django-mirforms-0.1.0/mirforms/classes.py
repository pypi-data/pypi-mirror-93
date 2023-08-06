class MirSelect:
    queryset = None
    filters = []
    template_name = "mirforms/widgets/htmx_select/htmx_select.html"
    option_template_name = "mirforms/widgets/htmx_select/htmx_select_option.html"
    htmx_attrs = {}

    def get_queryset(self):
        return self.queryset
