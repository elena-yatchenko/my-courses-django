from django.contrib import admin

# Register your models here.
from .models import Category, Course, Student, Payment, Review, Performance


@admin.register(Course)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class BookAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
# admin.site.register(Course)
admin.site.register(Performance)
# admin.site.register(Student)
admin.site.register(Payment)
#admin.site.register(Image)
# admin.site.register(Review)
