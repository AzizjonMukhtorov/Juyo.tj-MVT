from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass


class Category(models.Model):

    category_name = models.CharField(max_length=100)
    
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("Category_etail", kwargs={"pk": self.pk})
   

class Post(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=150,null=False, verbose_name = "Савол")
    image = models.ImageField(upload_to="posts/", null=True,blank=True, verbose_name = "Сурат")
    content = models.TextField(null= True,blank=True, verbose_name = "Шарҳ")
    date_created = models.DateTimeField(default=timezone.now,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name = "Категория")
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"pk": self.pk})
    
    def number_of_likes(self):
        return self.likes.count()


class Answer(models.Model):
    
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="posts/", null=True,blank=True, verbose_name = "Сурат")
    content = models.TextField(null= True,blank=True, verbose_name = "Посух")
    date_created = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(CustomUser, related_name='answer_likes', blank=True)


    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("Answer_detail", kwargs={"pk": self.pk})
    
    def number_of_likes(self):
        return self.likes.count()