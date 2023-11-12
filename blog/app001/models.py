from django.db import models
from django.contrib.auth.models import User
from django.db import models
from .utils import upload_to_post_images
from django.utils import timezone  # Import timezone
  # Import your upload_to_post_images function
from django.db.models.fields.files import ImageField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

def upload_to_post_images(instance, filename):
    return f'media/post_images/{instance.title}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to=upload_to_post_images, default='default_image.jpg')  # Add the default value

    def __str__(self):
        return self.title

    def set_tags(self, tags_str):
        tag_names = [tag.strip() for tag in tags_str.split(',')]
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            self.tags.add(tag)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.description}"

    def save(self, *args, **kwargs):
        # Set the date to the current date if it's not provided
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    source = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.source}"

    def save(self, *args, **kwargs):
        # Set the date to the current date if it's not provided
        if not self.date:
            self.date = timezone.now().date()
        super().save(*args, **kwargs)
