from django.contrib import admin
from .models import Institution, StatisticsSnapshot


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('otm_code', 'otm_name', 'ownership_type')
    search_fields = ('otm_code', 'otm_name')
    list_filter = ('ownership_type',)
    ordering = ('otm_code',)


@admin.register(StatisticsSnapshot)
class StatisticsSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        'institution__otm_code',
        'institution__otm_name',
        'institution__ownership_type',
        'bachelor_full_time',
        'bachelor_evening',
        'bachelor_part_time',
        'bachelor_special',
        'bachelor_joint',
        'bachelor_distance',
        'secondary_full_time',
        'secondary_evening',
        'secondary_part_time',
        'masters_full_time',
        'masters_evening',
        'masters_part_time',
        'masters_special',
        'masters_joint',
        'masters_distance',
        'total_students',
        'snapshot_date',
    )
    list_filter = ('snapshot_date', 'institution__ownership_type')
    search_fields = ('institution__otm_name', 'institution__otm_code')
    date_hierarchy = 'snapshot_date'

    fieldsets = (
        ('Institution Info', {
            'fields': ('institution', 'snapshot_date')
        }),
        ('Bachelor Statistics', {
            'fields': (
                'bachelor_full_time', 'bachelor_evening', 'bachelor_part_time',
                'bachelor_special', 'bachelor_joint', 'bachelor_distance'
            )
        }),
        ('Secondary Higher Education', {
            'fields': (
                'secondary_full_time', 'secondary_evening', 'secondary_part_time'
            )
        }),
        ('Master Statistics', {
            'fields': (
                'masters_full_time', 'masters_evening', 'masters_part_time',
                'masters_special', 'masters_joint', 'masters_distance'
            )
        }),
        ('Totals', {
            'fields': ('total_students',)
        }),
    )
    readonly_fields = ('total_students',)
