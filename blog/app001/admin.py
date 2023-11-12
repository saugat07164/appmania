from django.contrib import admin
from django.db import models
from .models import Post, Expense, Income
from ckeditor.widgets import CKEditorWidget

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget(config_name='default')}
    }

admin.site.register(Post, PostAdmin)
admin.site.register(Expense)
admin.site.register(Income)
