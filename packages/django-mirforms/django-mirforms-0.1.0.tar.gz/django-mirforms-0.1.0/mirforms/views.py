import json
from importlib import import_module
from django.views import generic
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from mirforms.utils import decode
from django.db.models import Q
from functools import reduce
import operator


@method_decorator(csrf_exempt, name="dispatch")
class SelectInlineView(generic.TemplateView):
    def post(self, request, *args, **kwargs):
        """
        Htmx Select Search bar will post to this function
        with a URl containing coded params
            klass: HtmxSelect defined class that contains:
                    queryset, filters
        """
        params = json.loads(decode(request.GET.get("select", "")))

        # Retrieve the query to be used with filters
        query = request.POST.get("query", "")

        # Retrieve Htmx Class that contains queryset and filters
        htmx_class = getattr(
            import_module(params.get("module")), params.get("klass")
        )

        # Filter the queryset by query
        filtered_queryset = self.filter_queryset(
            htmx_class.queryset, htmx_class.filters, query
        )
        return render(
            request,
            "mirforms/widgets/htmx_select/htmx_select_wrapper.html",
            {
                "queryset": filtered_queryset,
                "option_template_name": htmx_class.option_template_name,
                "htmx_attrs": htmx_class.htmx_attrs,
                "widget_name": filtered_queryset.model.__name__,
            },
        )

    def filter_queryset(self, queryset, filters, query):
        # Build a list of Q filters
        or_queries = [Q(**{flt: query}) for flt in filters]
        # Filter the queryset and return top 10
        return queryset.filter(reduce(operator.or_, or_queries))[:10]
