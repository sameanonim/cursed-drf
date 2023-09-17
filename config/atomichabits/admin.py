from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'place', 'action', 'time',
        'execution_time', 'is_pleasurable',
        'is_public', 'linked_habit'
    )
    list_filter = ('user', 'is_public')
    search_fields = ('place', 'action')

    fieldsets = (
        ('Общее', {
            'fields': (
                'user', 'place', 'action',
                'time', 'execution_time'
            )
        }),
        ('Дополнительно', {
            'fields': (
                'is_public', 'is_pleasurable',
                'frequency', 'reward'
            ),
            'classes': ('collapse',)
        })
    )
