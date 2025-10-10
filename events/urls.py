from django.urls import path

from .views import (
    # Essential Admin Views
    EventCategoryListView,
    EventCategoryCreateView,
    EventCategoryUpdateView,
    EventCategoryDeleteView,
    EventCreateView,
    EventListView,
    EventUpdateView,
    EventDetailView,
    EventDeleteView,
    
    # Essential User Views
    JoinEventListView,
    UserEventListView,
    RemoveEventMemberDeleteView,
    RemoveEventUserWishDeleteView,
    CreateUserMark,
    
    # Public Views
    PublicEventListView,
    PublicEventDetailView,
    join_event,
    public_search_events,
    
    # Admin Message Views
    AdminMessageListView,
    AdminMessageDetailView,
    send_admin_message,
    contact_admin,
    UserMessagesView,
    
    # Event Comment Views
    EventDetailWithCommentsView,
    add_event_comment,
    reply_to_comment,
)

urlpatterns = [
    # ESSENTIAL ADMIN URLS - Event Management
    path('category-list/', EventCategoryListView.as_view(), name='event-category-list'),
    path('create-category/', EventCategoryCreateView.as_view(), name='create-event-category'),
    path('category/<int:pk>/edit/', EventCategoryUpdateView.as_view(), name='edit-event-category'),
    path('category/<int:pk>/delete/', EventCategoryDeleteView.as_view(), name='delete-event-category'),
    
    path('event-create/', EventCreateView.as_view(), name='event-create'),
    path('event-list/', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event-edit'),
    path('detail/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('delete/<int:pk>', EventDeleteView.as_view(), name='event-delete'),
    
    # ESSENTIAL USER URLS - Event Registration
    path('join-event-list/', JoinEventListView.as_view(), name='join-event-list'),  # Admin view - all registrations
    path('my-events/', UserEventListView.as_view(), name='user-events'),  # User view - only their events
    path('join/<int:event_id>/', join_event, name='join-event'),
    path('remove-member/<int:pk>/', RemoveEventMemberDeleteView.as_view(), name='remove-event-member'),
    path('remove-wish/<int:pk>/', RemoveEventUserWishDeleteView.as_view(), name='remove-event-user-wish'),
    path('create-user-mark/', CreateUserMark.as_view(), name='create-user-mark'),
    
    # PUBLIC URLS - No Authentication Required
    path('public/', PublicEventListView.as_view(), name='public-events'),
    path('public/<int:pk>/', PublicEventDetailView.as_view(), name='public-event-detail'),
    path('public/search/', public_search_events, name='public-search-events'),
    
    # ADMIN MESSAGE URLS
    path('admin/messages/', AdminMessageListView.as_view(), name='admin-message-list'),
    path('admin/messages/<int:pk>/', AdminMessageDetailView.as_view(), name='admin-message-detail'),
    path('send-message/', send_admin_message, name='send-admin-message'),
    path('contact/', contact_admin, name='contact-admin'),
    path('my-messages/', UserMessagesView.as_view(), name='user-messages'),
    
    # EVENT COMMENT URLS
    path('event/<int:pk>/comments/', EventDetailWithCommentsView.as_view(), name='event-detail-with-comments'),
    path('event/<int:event_id>/comment/', add_event_comment, name='add-event-comment'),
    path('comment/<int:comment_id>/reply/', reply_to_comment, name='reply-to-comment'),
]