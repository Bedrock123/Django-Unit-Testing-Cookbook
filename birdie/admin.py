from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('excerpt',)

    def excerpt(self, obj):
        return obj.get_excerpt(5)

admin.site.register(Post, PostAdmin)

