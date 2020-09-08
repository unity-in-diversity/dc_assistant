from django.contrib import admin, messages
from django.shortcuts import redirect, render
from .models import UserKey
from .forms import ActivateUserKeyForm
from dc_assistant.admin import admin_site


@admin.register(UserKey, site=admin_site)
class UserKeyAdmin(admin.ModelAdmin):
    actions = ['activate_selected']
    list_display = ['user', 'is_filled', 'is_active', 'created']
    fields = ['user', 'public_key', 'is_active', 'last_updated']
    readonly_fields = ['user', 'is_active', 'last_updated']

    def get_readonly_fields(self, request, obj=None):
        # Don't allow a user to modify an existing public key directly.
        if obj and obj.public_key:
            return ['public_key'] + self.readonly_fields
        return self.readonly_fields

    def get_actions(self, request):
        # Bulk deletion is disabled at the manager level, so remove the action from the admin site for this model.
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        if not request.user.has_perm('secrets.activate_userkey'):
            del actions['activate_selected']
        return actions

    def activate_selected(modeladmin, request, queryset):
        """
        Enable activation of UserKeys
        """
        print('request.user', request.user)
        try:
            my_userkey = UserKey.objects.get(user=request.user)
            print('my_userkey:', my_userkey)
        except UserKey.DoesNotExist:
            messages.error(request, "You do not have an active User Key.")
            return redirect('/admin/secret/userkey')

        if 'activate' in request.POST:
            form = ActivateUserKeyForm(request.POST)
            if form.is_valid():
                master_key = my_userkey.get_master_key(form.cleaned_data['secret_key'])
                print('if form valid - master_key:', master_key)
                if master_key is not None:
                    for uk in form.cleaned_data['_selected_action']:
                        print('each uk:', uk)
                        uk.activate(master_key)
                    return redirect('/admin/secret/userkey')
                else:
                    messages.error(
                        request, "Invalid private key provided. Unable to retrieve master key.", extra_tags='error'
                    )
        else:
            form = ActivateUserKeyForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(request, 'secret/activate_keys.html', {
            'form': form,
        })
    activate_selected.short_description = "Activate selected user keys"

