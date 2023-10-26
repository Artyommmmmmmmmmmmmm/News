from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        postR = 0
        postR += postRat.get('postRating')

        commRat = self.user.comment_set.aggregate(commRating=Sum('rating'))
        commR = 0
        commR += postRat.get('commRating')

        self.rating = postR*3 + commR
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NE'
    article_news=[
        (article, 'Статья'),
        (news, 'Новости')
    ]

    author = models.ForeignKey(Author, on_delete = models.CASCADE )
    post_type = models.CharField(max_length=2, choices = article_news, default= article )
    time_made = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=40)
    text = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 124:
            return self.text[0:123] + '...'
        else:
            return self.text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    text = models.CharField(max_length=255)
    time_made = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()