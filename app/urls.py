from django.urls import path
from .views import (PostView, PostDetailView, PostCreateView,PostUpdateView,
                    CustomUserCreateView,  CategoryView, CategoryDetailView, 
                    AnswerView,  AnswerCreateView, AnswerUpdateView, UserSignupView, UserLoginView, search_questioin, post_likes, answer_likes)
from django.contrib.auth.views import LogoutView

                   
urlpatterns = [

    path('',PostView.as_view(),name='home'),
    path('create-post/',PostCreateView.as_view(),name="post_create"),
    path('post-detail/<int:pk>/',PostDetailView.as_view(),name="post_detail"),
    path('post-update/<int:pk>/',PostUpdateView.as_view(),name="post_update"),

    path('create-user/',CustomUserCreateView.as_view(),name="create_user"),


    path('category-view/',CategoryView.as_view(),name='category_view'),
    path('category-detail/<int:pk>/',CategoryDetailView.as_view(),name="category_detail"),


    path('answer-view/',AnswerView.as_view(),name='anwer_view'),
    path('create-answer/<int:pk>/',AnswerCreateView.as_view(),name="create_answer"),
    path('answer-update/<int:pk>/',AnswerUpdateView.as_view(),name="answer_update"),

    path('login-user/', UserLoginView.as_view(), name="login"),
    path('registration-user/', UserSignupView.as_view(), name="registration"),
    path('logout/', LogoutView.as_view(next_page='home'), name="logout"),

    path('search_questioin', search_questioin, name='search-questioin'),

    path('post-likes/<int:pk>/', post_likes, name='post-likes'),
    path('answer-likes/<int:pk>/like/', answer_likes, name='answer-likes'),
]
