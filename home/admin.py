from django.contrib import admin

# Register your models here.
# admin.py

# admin.py

from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('-Overall_Score')
        return queryset

    def rank(self, obj):
        queryset = self.get_queryset(None)
        rank = list(queryset).index(obj) + 1
        return rank
    rank.short_description = 'Rank'

    list_display = ('name', 'Overall_Score', 'rank','Course')

admin.site.register(Student, StudentAdmin)



    