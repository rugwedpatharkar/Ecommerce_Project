from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Address, Profile

class AddressResource(resources.ModelResource):
    class Meta:
        model = Address

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):  # Use ImportExportModelAdmin here
    resource_class = AddressResource
    list_display = ('profile', 'address_line1', 'city', 'state', 'postal_code', 'country')
    search_fields = ('profile__user__username', 'address_line1', 'city', 'state', 'postal_code', 'country')
    list_filter = ('city', 'state', 'country')
    ordering = ('profile', 'city', 'state', 'postal_code', 'country')

class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile

@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin):  # Use ImportExportModelAdmin here
    resource_class = ProfileResource
    list_display = ('user', 'is_email_verified', 'contact_number')
    search_fields = ('user__username', 'contact_number')
    list_filter = ('is_email_verified',)
    ordering = ('user', 'is_email_verified')
