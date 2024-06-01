from django.contrib import admin

# Register your models here.
from .models import Category, Course, Student, Payment, Review, Performance


# class CourseInline(admin.StackedInline):
class CourseInline(admin.TabularInline):
    model = Course
    fields = [
        "name",
        "is_deleted",
        "rating",
        "lasting",
        "cost",
    ]
    readonly_fields = ["rating"]
    extra = 0
    ordering = ["-rating"]
    # fieldsets = [
    #     (
    #         None,
    #         {
    #             "fields": ["name", "is_deleted"],
    #         },
    #     ),
    #     (
    #         "Характиристики курса",
    #         {
    #             "classes": ["wide"],
    #             "fields": ["lasting", "cost", "rating"],
    #         },
    #     ),
    # ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "flag"]
    ordering = ["name"]
    list_per_page = 10
    search_fields = ["name"]
    inlines = [CourseInline]


class StudentInline(admin.TabularInline):
    model = Student
    fields = [
        "surname",
        "name",
        "status",
        "is_paid",
        "rest_of_payment",
        "reg_date",
        "is_deleted",
    ]
    readonly_fields = ["rest_of_payment", "is_paid"]
    extra = 0
    ordering = ["status"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "rating",
        "lasting",
        "cost",
        "total_cost",
        "views_num",
    ]
    # radio_fields = {"category": admin.VERTICAL}
    ordering = ["-rating"]
    list_per_page = 7
    search_fields = ["name"]
    list_filter = ["is_deleted", "category", "lasting"]
    inlines = [StudentInline]

    readonly_fields = ["rating", "views_num", "added"]
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "category", "is_deleted"],
            },
        ),
        (
            "Описание",
            {
                "classes": ["collapse"],
                "fields": ["summary", ("added", "views_num")],
            },
        ),
        (
            "Характеристики курса",
            {
                "classes": ["wide"],
                "fields": [("lasting", "cost")],
            },
        ),
        (
            "Прочее",
            {
                "classes": ["wide"],
                "fields": ["rating"],
            },
        ),
    ]


class PerformanceInline(admin.TabularInline):
    model = Performance
    extra = 0
    fields = [
        "mark",
        "date_of_mark",
    ]
    # radio_fields = {"mark": admin.HORIZONTAL}
    ordering = ["-date_of_mark"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "pk",
        "course",
        "status",
        "average_mark",
        "is_paid",
        "rest_of_payment",
        "related_user",
    ]
    radio_fields = {"status": admin.HORIZONTAL}
    ordering = ["status", "pk"]
    list_per_page = 7
    search_fields = ["surname", "name"]
    list_filter = ["is_deleted", "status", "course"]
    inlines = [PerformanceInline]

    readonly_fields = [
        "related_user",
        "request_date",
        "reg_date",
        "updated",
        "deleted",
        "is_paid",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ["surname", "name", "is_paid", "is_deleted"],
            },
        ),
        (
            "Личные данные",
            {
                "classes": ["collapse"],
                "fields": ["phone", "date_of_birth", "photo"],
            },
        ),
        (
            "Учеба",
            {
                "classes": ["wide"],
                "fields": ["course", "status"],
            },
        ),
        (
            "Прочее",
            {
                "classes": ["collapse"],
                "fields": [
                    ("request_date", "reg_date"),
                    ("updated", "deleted"),
                ],
            },
        ),
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "paid_date",
        "amount",
    ]
    ordering = ["student"]
    list_per_page = 10
    # search_fields = ["student"]
    list_filter = ["paid_date"]

    readonly_fields = ["added", "updated"]


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = [
        "mark",
        "student",
        "date_of_mark",
    ]
    ordering = ["student"]
    list_per_page = 10
    search_fields = ["mark"]
    list_filter = ["date_of_mark", "student"]

    readonly_fields = ["added", "updated"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "course",
        "rate",
        "get_summary",
    ]
    ordering = ["course", "-added"]
    list_per_page = 10
    search_fields = ["rate"]
    list_filter = ["course", "added"]

    readonly_fields = ["added", "rate", "text"]
    fieldsets = [
        (
            None,
            {
                "fields": ["rate", "course"],
            },
        ),
        (
            "Комментарий",
            {
                "classes": ["collapse"],
                "fields": ["text"],
            },
        ),
        (
            "Прочее",
            {
                "fields": ["added"],
            },
        ),
    ]


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Course)
# admin.site.register(Performance)
# admin.site.register(Student)
# admin.site.register(Payment)
# admin.site.register(Image)
# admin.site.register(Review)
