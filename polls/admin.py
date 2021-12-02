from django.contrib import admin
from .models import User, Question, Topic, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['creator', 'question_text', 'topic']}), ]
    inlines = [ChoiceInline]


class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'first_name', 'last_name', 'username', 'email', 'password', 'bio', 'avatar'
            ),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
