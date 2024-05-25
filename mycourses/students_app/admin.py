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
    # fields = [
    #     "surname",
    #     "name",
    #     "status",
    #     "is_paid",
    #     "rest_of_payment",
    #     "reg_date",
    #     "is_deleted",
    # ]
    # readonly_fields = ["rest_of_payment", "is_paid"]
    # extra = 0
    # ordering = ["status"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "course",
        "status",
        "average_mark",
        "is_paid",
        "rest_of_payment",
        "related_user",
    ]
    radio_fields = {"status": admin.HORIZONTAL}
    ordering = ["surname", "status"]
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
                "fields": ["phone", "date_of_birth"],
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


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ["pk", "name", "price", "quantity", "describe"]
#     # actions = [filter_price, zero_quantity]
#     ordering = ["quantity", "name"]
#     list_per_page = 10
#     search_fields = ["describe"]
#     list_filter = ["added", "describe"]  # например, отфильтровать high cost продукты


#     readonly_fields = ["added", "updated"]
#     fieldsets = [
#         (
#             "Товар",
#             {
#                 "classes": ["wide"],
#                 "fields": ["name"],
#             },
#         ),
#         (
#             "Описание",
#             {
#                 "classes": ["collapse"],
#                 "description": "Описание товара",
#                 "fields": ["describe"],
#             },
#         ),
#         (
#             "Данные для реализации",
#             {
#                 "fields": ["price", "quantity"],
#             },
#         ),
#         (
#             "Прочее",
#             {
#                 "classes": ["collapse"],
#                 "fields": ["added", "updated"],
#             },
#         ),
#     ]


@admin.register(Review)
class BookAdmin(admin.ModelAdmin):
    pass


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Course)
admin.site.register(Performance)
# admin.site.register(Student)
admin.site.register(Payment)
# admin.site.register(Image)
# admin.site.register(Review)
