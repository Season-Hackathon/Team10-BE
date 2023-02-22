from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, CustomUser
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

class AccountAdmin(UserAdmin):

    list_display = ('username', 'email', 'phone_num')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'phone_num')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'hone_num', 'password')}
         ),
    )
    search_fields = ('email','username')
    ordering = ('username',)
    filter_horizontal = ()

#admin 의 기본 User모델 등록 취소
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

admin.site.register(CustomUser, AccountAdmin)