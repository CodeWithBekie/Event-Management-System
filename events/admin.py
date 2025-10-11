from django.contrib import admin

from .models import (
    EventCategory,
    Event,
    JobCategory,
    EventJobCategoryLinking,
    EventMember,
    EventUserWishList,
    UserCoin,
    AdminMessage,
    EventComment,
)


@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'sender_email', 'status', 'is_read', 'created_date']
    list_filter = ['status', 'is_read', 'created_date']
    search_fields = ['subject', 'sender__username', 'sender_email', 'message']
    readonly_fields = ['sender', 'sender_email', 'ip_address', 'user_agent', 'created_date']
    date_hierarchy = 'created_date'
    
    fieldsets = (
        ('Message Info', {
            'fields': ('sender', 'sender_email', 'subject', 'message')
        }),
        ('Status & Response', {
            'fields': ('status', 'is_read', 'responded_by', 'response', 'response_date')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent', 'created_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'comment_preview', 'created_date', 'is_approved', 'status']
    list_filter = ['status', 'is_approved', 'created_date', 'event']
    search_fields = ['comment', 'user__username', 'event__name']
    readonly_fields = ['created_date', 'updated_date']
    date_hierarchy = 'created_date'
    
    def comment_preview(self, obj):
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Comment Preview'


admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(JobCategory)
admin.site.register(EventJobCategoryLinking)
admin.site.register(EventMember)
admin.site.register(EventUserWishList)
admin.site.register(UserCoin)
