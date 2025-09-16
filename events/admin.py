from django.contrib import admin

from .models import (
    EventCategory,
    Event,
    JobCategory,
    EventJobCategoryLinking,
    EventMember,
    EventUserWishList,
    UserCoin,
)

admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(JobCategory)
admin.site.register(EventJobCategoryLinking)
admin.site.register(EventMember)
admin.site.register(EventUserWishList)
admin.site.register(UserCoin)
