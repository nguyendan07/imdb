from django.views.generic import (ListView, DetailView)

from .models import Movie


class MovieList(ListView):
    model = Movie
    paginate_by = 10


class MovieDetail(DetailView):
    model = Movie
