import datetime
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy, reverse, resolve
from boards.models import Board, Topic, Post
from boards.forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, CreateView, UpdateView
from django.db.models import Count

# Create your views here.
class HomeView(ListView):
    model = Board # board_list.html
    template_name = 'boards/home.html'
    context_object_name = 'boards'

def board_detail(request, board_name):
    board = Board.objects.get(name = board_name)
    topics = board.topics.all().annotate(replies=Count('posts') - 1)
    data = {'board': board, 'topics': topics}
    return render(request, 'boards/board_detail.html', data)

@login_required
def new_topic(request, board_name):
    board = Board.objects.get(name = board_name)
    data = {'board': board}
    if request.method == 'GET':
        form = NewTopicForm()
        data['form'] = form
        return render(request, 'boards/new_topic.html', data)
    elif request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            form_data = request.POST
            subject = form_data['subject']
            message = form_data['message']
            topic = Topic.objects.create(subject=subject, board=board, starter=request.user)
            Post.objects.create(message=message, topic=topic, created_by=request.user)
            return redirect("boards:board_detail", board_name)

def topic_posts(request, board_name, pk):
    topic = Board.objects.get(name=board_name).topics.get(pk=pk)
    topic.views += 1
    topic.save()
    data = {'topic':topic}
    return render(request, 'boards/topic_posts.html', data)

# @login_required
# def reply_topic(request, board_name, pk):
#     topic = Board.objects.get(name=board_name).topics.get(pk=pk)
#     data = {'topic': topic}
#     if request.method == 'GET':
#         form = PostForm()
#         data['form'] = form
#     elif request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.topic = topic
#             post.created_by = request.user
#             post.save()
#             return redirect('boards:topic_posts', board_name=board_name, pk=pk)
#     return render(request, 'boards/reply_topic.html', data)

class ReplyTopicView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('boards:home')
    template_name = 'boards/reply_topic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = Topic.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user
        post.topic = Topic.objects.get(pk=self.kwargs['pk'])
        post.save()
        return redirect('boards:topic_posts', board_name=post.topic.board.name, pk=post.topic.pk)

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_at = datetime.datetime.now()
        post.updated_by = self.request.user
        post.save()
        return redirect('boards:topic_posts', board_name=post.topic.board.name, pk=post.topic.pk)

def about(request):
    return render(request, '/boards/about.html')
