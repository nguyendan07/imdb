import django

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic import (CreateView, DetailView, ListView, UpdateView)

from .forms import (MovieImageForm, VoteForm)
from .mixins import CachePageVaryOnCookieMixin
from .models import Movie, Person, Vote


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class MovieList(CachePageVaryOnCookieMixin, ListView):
    model = Movie
    paginate_by = 10


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_related_person_and_score()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(user=self.request.user,
                                                               movie=self.object)
            if vote.id:
                vote_form_url = reverse('core:UpdateVote',
                                        kwargs={'movie_id': vote.movie.id, 'pk': vote.id})
            else:
                vote_form_url = reverse('core:CreateVote', kwargs={'movie_id': self.object.id})
            
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx
    
    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None


class MovieImageUpload(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial
    
    # def get_success_url(self):
    #     movie_id = self.kwargs['movie_id']
    #     movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
    #     return redirect(movie_detail_url)
    
    # def render_to_response(self, context, **response_kwargs):
    #     movie_id = self.kwargs['movie_id']
    #     movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
    #     return redirect(movie_detail_url)
    
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})
    
    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(movie_detail_url)


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial
    
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})
    
    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(movie_detail_url)


class TopMovies(ListView):
    template_name = 'core/top_movies_list.html'
    
    def get_queryset(self):
        limit = 10
        key = 'top_movies_%s' % limit
        cached_qs = cache.get(key)
        if cached_qs:
            same_django = cached_qs._django_version == django.get_version()
            if same_django:
                return cached_qs
        qs = Movie.objects.top_views(limit=limit)
        cache.set(key, qs)
        return qs    


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another users vote')
        return vote
    
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})
    
    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(movie_detail_url)
