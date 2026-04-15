from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'gender', 'age', 'age_group',
        'country_id', 'gender_probability', 'country_probability', 'created_at'
    )
    list_filter = ('gender', 'age_group', 'country_id')
    search_fields = ('name', 'country_id')
    ordering = ('-created_at',)
    readonly_fields = (
        'id', 'name', 'gender', 'gender_probability', 'sample_size',
        'age', 'age_group', 'country_id', 'country_probability', 'created_at'
    )

    def has_add_permission(self, request):
        return False  