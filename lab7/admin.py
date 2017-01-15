from django.contrib import admin

# Register your models here.

from lab7.models import Lesson, MyUser

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name','description','datetime','desc_len')
    list_filter = ['datetime']
    search_fields = ('id','name')
    
    def desc_len(self, obj):
        return len(obj.description)
    desc_len.short_description = "Длина сообщения"

admin.site.register(Lesson, LessonAdmin)

class MyUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(MyUser, MyUserAdmin)
