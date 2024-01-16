from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from .models import SchoolForm
from django.utils import timezone
from .models import Message
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.db.models import Count

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
admin.site.register(CustomUser, CustomUserAdmin)


# admin.py

class CustomStatusFilter(admin.SimpleListFilter):
    title = _('Custom Status')
    parameter_name = 'custom_status'

    def lookups(self, request, model_admin):
        return (
            ('ongoing', _('Ongoing')),
            ('completed', _('Completed')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'ongoing':
            return queryset.filter(status='Ongoing')
        elif self.value() == 'completed':
            return queryset.filter(status='Completed')
        

class SchoolFormAdmin(admin.ModelAdmin):

    list_display = ('get_unique_id', 'get_full_name', 'user_type', 'requestform', 'formatted_request_date', 'custom_date_released', 'custom_status')
    search_fields = ('get_unique_id', 'status')
    list_filter = ('user_type', CustomStatusFilter)

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    get_full_name.short_description = 'Full Name'    

    def get_unique_id(self, obj):
        # Custom method to generate a unique ID based on the object's ID
        return f'F{obj.id:04d}'

    get_unique_id.short_description = 'Unique ID'

    def get_document_requested(self, obj):
        return obj.document_requested

    get_document_requested.short_description = 'Document Requested'

    def formatted_request_date(self, obj):
        return obj.request_date.strftime('%m-%d-%Y') if obj.request_date else "N/A"

    formatted_request_date.short_description = 'Request Date'

    def custom_date_released(self, obj):
        return obj.date_released.strftime('%m-%d-%Y') if obj.date_released else "N/A"

    custom_date_released.short_description = 'Date Released'

    def custom_status(self, obj):
        return obj.status

    custom_status.short_description = 'Status'


    def get_actions(self, request):
        # Disable delete selected action
        actions = super().get_actions(request)
        del actions['delete_selected']
        return actions

    actions = ['mark_as_ongoing', 'mark_as_completed']

    def mark_as_ongoing(modeladmin, request, queryset):
        # Custom action to mark selected forms as ongoing
        queryset.update(status='Ongoing', date_released=None)  # Set date_released to None for ongoing forms

    mark_as_ongoing.short_description = "Mark selected as ongoing"

    def mark_as_completed(modeladmin, request, queryset):
        # Custom action to mark selected forms as completed
        queryset.update(status='Completed', date_released=timezone.now())

    mark_as_completed.short_description = "Mark selected as completed"

 

admin.site.register(SchoolForm, SchoolFormAdmin)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3})}

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'content', 'get_chats')
    search_fields = ('sender__username', 'recipient__username', 'content')
    readonly_fields = ('get_chats',)

    def get_chats(self, obj):
        # Fetch messages between admin and the sender (user)
        admin_user = get_user_model().objects.filter(is_staff=True).first()
        user_messages = Message.objects.filter(sender=obj.sender, recipient=admin_user)
        admin_messages = Message.objects.filter(sender=admin_user, recipient=obj.sender)
        # Combine and order messages
        messages = user_messages.union(admin_messages).order_by('timestamp')
        # Display messages in a simple format
        chat_history = '<br>'.join(
            f'{message.sender.username} - {message.timestamp}: {message.content}' for message in messages
        )
        
        # Display form for admin to reply
        reply_form = ReplyForm()
        return format_html('{}<br><br>{}', chat_history, reply_form)

    get_chats.short_description = 'Chat History'

    def save_model(self, request, obj, form, change):
        # Save the sender (admin) and recipient before saving the message
        obj.sender = get_user_model().objects.filter(is_staff=True).first()
        obj.recipient = form.cleaned_data['recipient']
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        # Redirect to the admin chat view after replying to a message
        return super().response_add(request, obj, post_url_continue='/admin_chat/{}/'.format(obj.sender.id))

# Register the MessageAdmin class for the Message model
admin.site.register(Message, MessageAdmin)