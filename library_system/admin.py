from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

class CustomAdminSite(admin.AdminSite):
    def logout(self, request, extra_context=None):
        # First perform the logout using the parent method
        response = super().logout(request, extra_context)
        # Then redirect to our custom home page
        return redirect('fbc_books:home')
