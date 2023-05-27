from django.contrib import admin

# Register your models here.

from .models import Post,Author,Tag,Comment

class CommmentAdmin(admin.ModelAdmin):
    list_display = ("text","post",)


admin.site.register(Comment,CommmentAdmin)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Tag)