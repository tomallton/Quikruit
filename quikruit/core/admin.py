from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from .models import QuikruitAccount
from .forms import AccountCreationForm

class QuikruitAccountAdmin(auth_admin.UserAdmin):
	form = AccountCreationForm
	add_form = AccountCreationForm

	list_display = ('email', 'is_active', 'is_superuser')
	list_filter = ('is_superuser', )
	fieldsets = (
		('Authentication info', {'fields': ('model_id', 'email',)}),
		('Privileges', {'fields': ('is_superuser',)}),
		(None, {'fields': ('is_active',)})
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password', 'password_conf')
			}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	readonly_fields = ('model_id',)
	filter_horizontal = ()

admin.site.register(QuikruitAccount, QuikruitAccountAdmin)