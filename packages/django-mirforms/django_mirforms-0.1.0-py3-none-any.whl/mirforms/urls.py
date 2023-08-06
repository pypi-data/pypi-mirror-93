from django.urls import path
from mirforms import views

app_name = "mirforms"
urlpatterns = [
    path(
        "",
        views.SelectInlineView.as_view(),
        name="select_inlines",
    ),
]
