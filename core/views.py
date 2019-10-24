from django.views.generic import (ListView, DetailView)

from .models import Person, Movie


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class MovieList(ListView):
    model = Movie
    paginate_by = 10


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_related_person()
