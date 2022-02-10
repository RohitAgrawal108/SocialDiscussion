from django.contrib import admin
from .models import Complaint, Category
# Register your models here.


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('against', 'description', 'owner', 'category', 'date','complaint_date','state')
    search_fields = ('description', 'category', 'date',)

    list_per_page = 5


admin.site.register(Complaint, ComplaintAdmin) 
admin.site.register(Category)
