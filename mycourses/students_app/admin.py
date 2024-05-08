from django.contrib import admin

# Register your models here.
from .models import Category, Course, Mark, Student, Payment, Review


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
admin.site.register(Mark)
# admin.site.register(Student)
admin.site.register(Payment)
# admin.site.register(Review)
