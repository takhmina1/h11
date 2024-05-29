from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RollRequest

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'phone', 'first_name', 'last_name', 'email', 'user_roll', 'roll_request')
    list_filter = ('user_roll', 'roll_request')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('code', 'activated', 'bonus_id', 'bonus', 'qrimg',
                                      'notification', 'auto_brightness', 'birthday', 'gender',
                                      'language', 'married', 'status', 'city', 'children',
                                      'animal', 'car', 'user_roll', 'roll_request')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(RollRequest)
