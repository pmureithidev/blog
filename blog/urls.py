from django.urls import path
from .views import PostListView, PostDetailView, EmailPostFormView, CommentCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/share/', EmailPostFormView.as_view(), name='share-post'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='add-comment'),
]
