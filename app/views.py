from django.shortcuts import redirect, render, get_object_or_404
from .models import CustomUser, Post, Answer, Category
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .form import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Count




#1~
class PostView(generic.ListView):
    model = Post
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()   
        context['post_list'] = Post.objects.all().annotate(like_count=Count('likes')).order_by('-like_count')
        return context
    
class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()  # Get the post object
        related_answers = Answer.objects.filter(post=post).annotate(like_count=Count('likes')).order_by('-like_count')
        answer_likes = {answer.id: answer.likes.count() for answer in related_answers}
        
        context['category_list'] = Category.objects.all().order_by("-id")
        context['post'] = post  # Pass post object to the context
        context['answer_count'] = related_answers.count()
        context['related_answers'] = related_answers
        context['post_likes'] = post.likes.count()
        context['answer_likes'] = answer_likes
        
        return context

class PostCreateView(generic.CreateView):
    model = Post
    template_name = "post.html"
    fields = ["title", "category", "image", "content"]
    success_url = reverse_lazy("home")

    def form_valid(self, form):

        if not self.request.user.is_authenticated:
            form.add_error(None, 'Аввал ворид шавед!')
            return self.form_invalid(form)
        
        form.instance.user = self.request.user

        return super().form_valid(form)

class PostUpdateView(generic.UpdateView):
    model = Post
    template_name = ""
    fields = "__all__" 
    success_url = reverse_lazy("")


class CustomUserCreateView(generic.CreateView):
    model = CustomUser
    template_name = ""
    fields = "__all__"
    success_url = reverse_lazy("")


#3
class CategoryView(generic.ListView):
    model = Category
    template_name = 'base.html'

    

    

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "category_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()  # Get the category object
        context['category_list'] = Category.objects.all().order_by("-id")
        context['category'] = category  # Pass category object to the context
        context['post_count'] = Post.objects.filter(category=category).count()
        context['related_posts'] = Post.objects.filter(category=category)
        return context


#4
class AnswerView(generic.ListView):
    model = Answer
    template_name = 'base.html'
    
    

class AnswerCreateView(generic.CreateView):
    model = Answer
    template_name = "create_answer.html"
    fields = ['image','content']
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        
        if not self.request.user.is_authenticated:
            form.add_error(None, 'Аввал ворид шавед!')
            return self.form_invalid(form)
        
        # Get the post object using the pk from the URL
        post = Post.objects.get(pk=self.kwargs['pk'])
        # Set the post field of the form instance
        form.instance.post = post
        # Set the user field if needed
        form.instance.user = self.request.user
        # Call the parent form_valid method to save the form
        return super().form_valid(form)
    

class AnswerUpdateView(generic.UpdateView):
    model = Answer
    template_name = "update_answer.html"
    fields = "__all__" 
    success_url = reverse_lazy("home")


#User authentication
class UserLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class UserSignupView(generic.FormView):
    template_name = 'registration.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserSignupView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        else:
            return super(UserSignupView, self).get(*args, **kwargs)


def search_questioin(request):
    search_result = []
    searched = ""
    
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()
        if searched:
            search_result = Post.objects.filter(title__icontains=searched).annotate(likes_count=Count('likes'))


        return render(request, 'search.html', 
                      {'search_result': search_result, 'searched': searched}, 
                    ) 
    else:
        context = {'category_list': Category.objects.all().order_by("-id")}
        return render(request, 'search.html', context)
    

def post_likes(request, pk):
    
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('home')
    else:
        messages.success(request, "You must login")
        return redirect('home')


def answer_likes(request, pk):
    if request.user.is_authenticated:
        answer = get_object_or_404(Answer, id=pk)
        if request.user in answer.likes.all():
            answer.likes.remove(request.user)
        else:
            answer.likes.add(request.user)
        return redirect('post_detail', pk=answer.post.id)  # Assuming 'post_detail' needs the post ID
    else:
        messages.success(request, "You must log in")
        return redirect('post_detail', pk=answer.post.id)