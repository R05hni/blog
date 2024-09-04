from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import SignupAPIView, LoginAPIView, LogoutAPIView, userbloglist

urlpatterns = [
    path('home', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('signup', views.signup, name='signup'),
    path('post/new/', views.create_post, name='create_post'),
    path('', views.login_view, name='login'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike-post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('download-post/<int:post_id>/', views.download_post, name='download_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('export-data', views.exportData, name='exportData'),
   
    path('password-update-api', views.update_passwordapi, name='update_password_api'),
    path('all-post-api', views.allBlogPostApi, name='all_post_api'),
    path('userpostlist', userbloglist.as_view(), name='bloglistapi'),
    path('createPostApi', views.createPostApi, name='create_post_api'),
    path('updatePostApi/<int:post_id>/', views.updatePostApi, name='update_post_api'),
    path('commentApi/<int:post_id>/', views.commentApi, name='comment_api'),
    path('deletePostApi/<int:comment_id>/', views.deleteCommentApi, name='delete_post_api'),
    path('updateCommentApi/<int:comment_id>/', views.updateCommentApi, name='update_comment'),
    path('interactionapi', views.InteractionApi, name='like-dislikeapi'),
    #path('dislikeapi', views.dislikePostApi, name='dislikeapi'),
    path('api/signup/', SignupAPIView.as_view(), name='signupapi'),
    path('api/login/', LoginAPIView.as_view(), name='loginapi'),
    path('api/logout/', LogoutAPIView.as_view(), name='logoutapi'),

]

