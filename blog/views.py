from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView


from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

# Create your views here.

# homepage view
class PostListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'home.html'

    def get_queryset(self):
        return Post.objects.filter(
            status=Post.Status.PUBLISHED
        )
    

# individual post view
class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'

    def get_object(self, queryset = None):
        # get params from URL
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['slug']

        # find the post using date and slug
        queryset = Post.objects.filter(
            status=Post.Status.PUBLISHED
        )

        # comments in posts
        form = CommentForm()

        return get_object_or_404(queryset,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,
                                 slug=slug)
    
# share posts via email view
class EmailPostFormView(FormView):
    template_name = "share_post.html"
    form_class = EmailPostForm
    success_url = reverse_lazy('post-list')

    # getting the post by id
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # passing the post ot the template
        context['post'] = Post.objects.get(id=self.kwargs['pk'])
        return context
    
    # form fields passed evaluation
    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs['pk'])
        
        # prepare the email content
        cleaned_data = form.cleaned_data
        subject = f"{cleaned_data['name']} recommends you read: {post.title}"
        message = (f"\n\nRead '{post.title}' at {self.request.build_absolute_uri(post.get_absolute_url())}\n\n"
                   f"{cleaned_data['name']}'s comments: {cleaned_data['comments']}")
        
        # success message
        messages.success(
            self.request,
            f"Post '{post.title} was sent to {cleaned_data['to']}"
        )
        
        # send email
        send_mail(
            subject,
            message,
            cleaned_data['email'],
            [cleaned_data['to']],
            fail_silently=False,
        )

        return super().form_valid(form)

# add comments view
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'
    success_url = reverse_lazy('post-detail')