from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView,CreateView, UpdateView, DeleteView

from saaf.gemini import get_gemini_client
from .models import Post, Comment, Event, Participation
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, EventForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from geopy.geocoders import Nominatim
from django.db.models import F, OuterRef, Subquery
from geopy.distance import geodesic
from django.utils import timezone

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .gemini import get_gemini_client

@csrf_exempt
def enhance_story(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content", "")
        genai = get_gemini_client()
        model = genai.GenerativeModel("models/gemini-flash-latest")
        try:
            response = model.generate_content(f"Rewrite the following content into a single improved version. Output only the improved text:\n\n{content}")
            enhanced = response.text or content
        except Exception as e:
            print("GEMINI ERROR:", str(e))
            enhanced = content
        return JsonResponse({"enhanced": enhanced})




# Create your views here.
def index(request):
    return render(request, "saaf/index.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "saaf/register.html", {"form":form})

@login_required
def profile(request):
    # joined_events = Event.objects.filter(participants__user=request.user)
    participation = Participation.objects.filter(
        event=OuterRef('pk'),
        user=request.user
    ).values('joined_at')[:1]
    joined_events = Event.objects.filter(participants__user=request.user).annotate(
        joined_at=Subquery(participation)
    )
    return render(request, "saaf/profile.html", {"user": request.user, "joined_events": joined_events})

    
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    return render(request, 'saaf/user_profile.html', {'profile_user': user, 'posts': posts})


#crud style views for Post model

#study this view in detail later (pleaseeeeeeeee) - Done!
class PostDetailView(DetailView):
    model = Post
    template_name = 'saaf/post_detail.html'
    context_object_name = "post"
    #for get method on the comments
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.order_by('-created_at')
        return context
    #for post method on the comments
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['form'] = form
        return self.render_to_response(context)


class PostListView(ListView):
    model = Post
    template_name = "saaf/post_list.html"
    context_object_name = "posts"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "saaf/post_form.html"
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('post-list')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class MyPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'saaf/my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Only show posts authored by the logged-in user
        return Post.objects.filter(author=self.request.user)
    
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied 
    post.delete()
    return redirect('my-posts')

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        raise PermissionDenied 
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post-detail', pk=post_pk)

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


#events from here on

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "saaf/event_form.html"
    form_class = EventForm

    def dispatch(self, request, *args, **kwargs):
        self.related_post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    #geolocation logic added here
    def form_valid(self, form):
        location = form.cleaned_data['location_name']
        geolocator = Nominatim(user_agent="saaf-event-locator")
        geo = geolocator.geocode(location)
        if geo:
            form.instance.latitude = geo.latitude
            form.instance.longitude = geo.longitude
        form.instance.post = self.related_post
        return super().form_valid(form)   


    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.related_post.pk})


def nearby_events(request):
    lat = float(request.GET.get('lat'))
    lng = float(request.GET.get('lng'))
    all_events = Event.objects.exclude(latitude=None).exclude(longitude=None)

    nearby = []
    for event in all_events:
        dist = geodesic((lat, lng), (event.latitude, event.longitude)).km
        if dist <= 10:  # 10 km radius
            nearby.append(event)

    return render(request, 'saaf/nearby_events.html', {'events': nearby})

class EventDetailView(DetailView):
    model = Event
    template_name = 'saaf/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        is_past = event.date < timezone.now()
        context['is_past'] = is_past
        context['user_has_joined'] = Participation.objects.filter(
            event=event, user=self.request.user
        ).exists()
        context['participants'] = Participation.objects.filter(event=event).select_related('user')
        return context

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.post.author != request.user:
        raise PermissionDenied
    post_pk = event.post.pk
    event.delete()
    return redirect('post-detail', pk=post_pk)

@login_required
@require_POST
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.date < timezone.now():
        return HttpResponseForbidden("You can't modify participation for past events.")

    Participation.objects.get_or_create(user=request.user, event=event)
    return redirect('event-detail', pk=pk)

@login_required
@require_POST
def cancel_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.date < timezone.now():
        return HttpResponseForbidden("You can't modify participation for past events.")
    Participation.objects.filter(user=request.user, event=event).delete()
    return redirect('event-detail', pk=pk)
    
def search_events_by_location(request):
    query = request.GET.get('location')
    geolocator = Nominatim(user_agent="saaf-location-search")
    geo = geolocator.geocode(query)

    if geo:
        lat, lng = geo.latitude, geo.longitude
        all_events = Event.objects.exclude(latitude=None).exclude(longitude=None)
        nearby = [
            event for event in all_events
            if geodesic((lat, lng), (event.latitude, event.longitude)).km <= 10
        ]
    else:
        nearby = []

    return render(request, 'saaf/search_results.html', {'events': nearby, 'query': query})



