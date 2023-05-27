from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Tag(models.Model):
    captions = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("tag_detail", args=[self.captions])
    

    def __str__(self):
        return self.captions

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()
    
    def get_absolute_url(self):
        return reverse("author_detail", args=[self.first_name])
    
    def get_Full_name(self):
        return f"{self.first_name}{self.last_name}"
    
    def __str__(self):
        return self.first_name

class Post(models.Model):
    title= models.CharField(max_length=100)
    excerpt = models.CharField(max_length=250)
    image = models.ImageField(upload_to='posts',null=True)
    content = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE , related_name="posts")
    tags = models.ManyToManyField(Tag,related_name='posts')
    date = models.DateField( auto_now=True)
    slug = models.SlugField(null=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        return super().save()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])
    

class Comment(models.Model):
    username = models.CharField(max_length=100)
    email_address = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")