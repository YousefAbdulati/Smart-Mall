from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name', 'image', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password','image')}),
      ('Personal info', {'fields': ('name', )}),
      ('Permissions', {'fields': ('is_admin',)}),
  )

  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'password1', 'password2' , 'image', 'gender', 'nationality' , 'address', 'phone' ,'date_of_birth','is_admin'),

      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)