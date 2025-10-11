from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to require admin/staff access"""
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You need administrator privileges to access this page.')
            return redirect('user-dashboard')
        return redirect('login')

from .models import (
    EventCategory,
    Event,
    JobCategory,
    EventJobCategoryLinking,
    EventMember,
    EventUserWishList,
    UserCoin,
    EventImage,
    EventAgenda,
    AdminMessage,
    EventComment

)
from .forms import EventForm, EventImageForm, EventAgendaForm, EventCreateMultiForm, AdminMessageForm, AdminMessageResponseForm, EventCommentForm, ContactForm


# ADMIN-ONLY VIEWS - Event Category Management
class EventCategoryListView(AdminRequiredMixin, ListView):
    model = EventCategory
    template_name = 'events/event_category.html'
    context_object_name = 'event_category'


class EventCategoryCreateView(AdminRequiredMixin, CreateView):
    model = EventCategory
    fields = ['name', 'code', 'image', 'priority', 'status']
    template_name = 'events/create_event_category.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


class EventCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = EventCategory
    fields = ['name', 'code', 'image', 'priority', 'status']
    template_name = 'events/edit_event_category.html'


class EventCategoryDeleteView(AdminRequiredMixin, DeleteView):
    model =  EventCategory
    template_name = 'events/event_category_delete.html'
    success_url = reverse_lazy('event-category-list')

@login_required(login_url='login')
def create_event(request):
    event_form = EventForm()
    event_image_form = EventImageForm()
    event_agenda_form = EventAgendaForm()
    catg = EventCategory.objects.all()
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        event_image_form = EventImageForm(request.POST, request.FILES)
        event_agenda_form = EventAgendaForm(request.POST)
        if event_form.is_valid() and event_image_form.is_valid() and event_agenda_form.is_valid():
            ef = event_form.save()
            # Set created and updated user
            ef.created_user = request.user
            ef.updated_user = request.user
            ef.save()
            
            event_image_form.save(commit=False)
            event_image_form.event_form = ef
            event_image_form.save()
            
            event_agenda_form.save(commit=False)
            event_agenda_form.event_form = ef
            event_agenda_form.save()
            return redirect('event-list')
    context = {
        'form': event_form,
        'form_1': event_image_form,
        'form_2': event_agenda_form,
        'ctg': catg
    }
    return render(request, 'events/create.html', context)

class EventCreateView(AdminRequiredMixin, CreateView):
    form_class = EventCreateMultiForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('event-list')

    def form_invalid(self, form):
        print("Form is INVALID!")
        for form_name, form_instance in form.forms.items():
            if form_instance.errors:
                print(f"Errors in {form_name}: {form_instance.errors}")
        return super().form_invalid(form)

    def form_valid(self, form):
        try:
            print("Form is valid, attempting to save event...")
            evt = form['event'].save(commit=False)
            # Set the user fields
            evt.created_user = self.request.user
            evt.updated_user = self.request.user
            # Ensure the event is active by default
            if not evt.status:
                evt.status = 'active'
            print(f"Saving event: {evt.name} with status: {evt.status}")
            evt.save()
            print(f"Event saved successfully with ID: {evt.id}")
            
            # Save event image if provided
            if form['event_image'].cleaned_data.get('image'):
                event_image = form['event_image'].save(commit=False)
                event_image.event = evt
                event_image.save()
                print("Event image saved")
            
            # Save event agenda if provided
            event_agenda = form['event_agenda'].save(commit=False)
            event_agenda.event = evt
            event_agenda.save()
            print("Event agenda saved")
            
            print("Redirecting to event list...")
            return redirect(self.success_url)
            
        except Exception as e:
            print(f"Error saving event: {e}")
            # Add error to form and return to form page
            form.add_error(None, f"Error saving event: {e}")
            return self.form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['ctg'] = EventCategory.objects.all()
        return context


# ADMIN-ONLY VIEWS - Event Management
class EventListView(AdminRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'


class EventUpdateView(AdminRequiredMixin, UpdateView):
    model = Event
    fields = ['category', 'name', 'description', 'scheduled_status', 'venue', 'start_date', 'end_date', 'location', 'points', 'maximum_attende', 'status']
    template_name = 'events/edit_event.html'


class EventDetailView(AdminRequiredMixin, DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventDeleteView(AdminRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/delete_event.html'
    success_url = reverse_lazy('event-list')


class AddEventMemberCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventMember
    fields = ['event', 'user', 'attend_status', 'status']
    template_name = 'events/add_event_member.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


class JoinEventListView(LoginRequiredMixin, ListView):
    """Admin view to see all event registrations - ADMIN ONLY"""
    login_url = 'login'
    model = EventMember
    template_name = 'events/joinevent_list.html'
    context_object_name = 'eventmember'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return all event members for admin view"""
        return EventMember.objects.all().order_by('-id')


class UserEventListView(LoginRequiredMixin, ListView):
    """View for regular users to see only their own registered events"""
    login_url = 'login'
    model = EventMember
    template_name = 'events/user_event_list.html'
    context_object_name = 'user_events'
    
    def get_queryset(self):
        """Return only events registered by the current user"""
        return EventMember.objects.filter(user=self.request.user)


class RemoveEventMemberDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventMember
    template_name = 'events/remove_event_member.html'
    success_url = reverse_lazy('user-events')
    
    def get_queryset(self):
        """Users can only delete their own event registrations"""
        if self.request.user.is_staff:
            # Admin can delete any registration
            return EventMember.objects.all()
        else:
            # Regular users can only delete their own registrations
            return EventMember.objects.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        """Ensure user can only access their own registrations"""
        obj = super().get_object(queryset)
        if not self.request.user.is_staff and obj.user != self.request.user:
            messages.error(self.request, 'Access denied. You can only manage your own registrations.')
            return redirect('user-events')
        return obj


class EventUserWishListView(LoginRequiredMixin, ListView):
    """Admin view to see all user wish lists - ADMIN ONLY"""
    login_url = 'login'
    model = EventUserWishList
    template_name = 'events/event_user_wish_list.html'
    context_object_name = 'eventwish'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return EventUserWishList.objects.all().order_by('-id')


class AddEventUserWishListCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = EventUserWishList
    fields = ['event', 'user', 'status']
    template_name = 'events/add_event_user_wish.html'

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


class RemoveEventUserWishDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = EventUserWishList
    template_name = 'events/remove_event_user_wish.html'
    success_url = reverse_lazy('user-events')
    
    def get_queryset(self):
        """Users can only delete their own wish list entries"""
        if self.request.user.is_staff:
            # Admin can delete any wish list entry
            return EventUserWishList.objects.all()
        else:
            # Regular users can only delete their own wish list entries
            return EventUserWishList.objects.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        """Ensure user can only access their own wish list entries"""
        obj = super().get_object(queryset)
        if not self.request.user.is_staff and obj.user != self.request.user:
            messages.error(self.request, 'Access denied. You can only manage your own wish list.')
            return redirect('user-events')
        return obj


class UpdateEventStatusView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    model = Event
    fields = ['status']
    template_name = 'events/update_event_status.html'


class CompleteEventList(LoginRequiredMixin, ListView):
    """Admin view to see all completed events - ADMIN ONLY"""
    login_url = 'login'
    model = Event
    template_name = 'events/complete_event_list.html'
    context_object_name = 'events'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Event.objects.filter(status='completed').order_by('-id')


class AbsenseUserList(LoginRequiredMixin, ListView):
    """Admin view to see absent users - ADMIN ONLY"""
    login_url = 'login'
    model = EventMember
    template_name = 'events/absense_user_list.html'
    context_object_name = 'absenseuser'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return EventMember.objects.filter(attend_status='absent').order_by('-id')


class CompleteEventUserList(LoginRequiredMixin, ListView):
    """Admin view to see users who completed events - ADMIN ONLY"""
    login_url = 'login'
    model = EventMember
    template_name = 'events/complete_event_user_list.html'
    context_object_name = 'completeuser'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return EventMember.objects.filter(attend_status='completed').order_by('-id')


class CreateUserMark(LoginRequiredMixin, CreateView):
    """Admin view to create user marks - ADMIN ONLY"""
    login_url = 'login'
    model = UserCoin
    fields = ['user', 'gain_type', 'gain_coin', 'status']
    template_name = 'events/create_user_mark.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_user = self.request.user
        form.instance.updated_user = self.request.user
        return super().form_valid(form)


class UserMarkList(LoginRequiredMixin, ListView):
    """Admin view to see all user marks - ADMIN ONLY"""
    login_url = 'login'
    model = UserCoin
    template_name = 'events/user_mark_list.html'
    context_object_name = 'usermark'
    
    def dispatch(self, request, *args, **kwargs):
        """Only allow admin/staff users to access this view"""
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('user-dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return UserCoin.objects.all().order_by('-id')


@login_required(login_url='login')
def search_event_category(request):
    if request.method == 'POST':
       data = request.POST['search']
       event_category = EventCategory.objects.filter(name__icontains=data)
       context = {
           'event_category': event_category
       }
       return render(request, 'events/event_category.html', context)
    return render(request, 'events/event_category.html')

@login_required(login_url='login')
def search_event(request):
    if request.method == 'POST':
       data = request.POST['search']
       events = Event.objects.filter(name__icontains=data)
       context = {
           'events': events
       }
       return render(request, 'events/event_list.html', context)
    return render(request, 'events/event_list.html')


# PUBLIC VIEWS FOR NON-AUTHENTICATED USERS

class PublicEventListView(ListView):
    """Public event listing that doesn't require authentication"""
    model = Event
    template_name = 'events/public_event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        return Event.objects.filter(status='active').order_by('-start_date')


class PublicEventDetailView(DetailView):
    """Public event detail view that doesn't require authentication"""
    model = Event
    template_name = 'events/public_event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(status='active')


@login_required(login_url='login')
def join_event(request, event_id):
    """Allow authenticated users to join an event"""
    event = get_object_or_404(Event, id=event_id, status='active')
    
    # Check if user is already registered
    existing_member = EventMember.objects.filter(event=event, user=request.user).first()
    
    if existing_member:
        messages.warning(request, 'You are already registered for this event.')
    else:
        # Check if event is full using our new method
        if event.is_full():
            messages.error(request, f'This event is full. Registration closed. ({event.get_registration_count()}/{event.maximum_attende} registered)')
        else:
            # Register user for event
            EventMember.objects.create(
                event=event,
                user=request.user,
                attend_status='waiting',
                status='active',
                created_user=request.user,
                updated_user=request.user
            )
            # Show updated count after registration
            new_count = event.get_registration_count() + 1  # +1 because we just added one
            messages.success(request, f'Successfully registered for {event.name}! ({new_count}/{event.maximum_attende} registered)')
    
    return redirect('public-event-detail', pk=event.id)


def public_search_events(request):
    """Public event search functionality"""
    events = Event.objects.filter(status='active').order_by('-start_date')
    
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        if search_query:
            events = events.filter(name__icontains=search_query)
    
    context = {
        'events': events,
        'search_query': request.POST.get('search', '') if request.method == 'POST' else ''
    }
    return render(request, 'events/public_event_list.html', context)


# ADMIN MESSAGES VIEWS
class AdminMessageListView(AdminRequiredMixin, ListView):
    """View for administrators to see all messages from users"""
    model = AdminMessage
    template_name = 'events/admin_message_list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        return AdminMessage.objects.all().select_related('sender', 'responded_by')


class AdminMessageDetailView(AdminRequiredMixin, DetailView):
    """View for administrators to see message details and respond"""
    model = AdminMessage
    template_name = 'events/admin_message_detail.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['response_form'] = AdminMessageResponseForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AdminMessageResponseForm(request.POST, instance=self.object)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.responded_by = request.user
            from django.utils import timezone
            message.response_date = timezone.now()
            message.is_read = True
            message.save()
            messages.success(request, 'Response sent successfully!')
            return redirect('admin-message-detail', pk=self.object.pk)
        
        context = self.get_context_data()
        context['response_form'] = form
        return self.render_to_response(context)


@login_required
def send_admin_message(request):
    """View for users to send messages to administrators"""
    if request.method == 'POST':
        form = AdminMessageForm(request.POST, user=request.user)
        if form.is_valid():
            # Get client IP and user agent for tracking
            ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            message = form.save(commit=False)
            message.ip_address = ip
            message.user_agent = user_agent
            message.save()
            
            messages.success(request, 'Your message has been sent to the administrators. We will respond as soon as possible.')
            return redirect('send-admin-message')
    else:
        form = AdminMessageForm(user=request.user)
    
    return render(request, 'events/send_admin_message.html', {'form': form})


def contact_admin(request):
    """View for anonymous users to contact admins"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create AdminMessage from contact form
            ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            AdminMessage.objects.create(
                sender=request.user if request.user.is_authenticated else None,
                sender_email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=f"Name: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nMessage:\n{form.cleaned_data['message']}",
                ip_address=ip,
                user_agent=user_agent
            )
            
            messages.success(request, 'Your message has been sent successfully. We will respond to your email address.')
            return redirect('contact-admin')
    else:
        form = ContactForm()
    
    return render(request, 'events/contact_admin.html', {'form': form})


# EVENT COMMENTS VIEWS
class EventDetailWithCommentsView(DetailView):
    """Enhanced event detail view with comments"""
    model = Event
    template_name = 'events/event_detail_with_comments.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Get comments for this event
        comments = EventComment.objects.filter(
            event=event, 
            status='active', 
            parent=None
        ).select_related('user').prefetch_related('replies')
        
        context['comments'] = comments
        context['comment_form'] = EventCommentForm()
        
        # Check if user is registered for this event
        if self.request.user.is_authenticated:
            context['is_registered'] = EventMember.objects.filter(
                event=event, 
                user=self.request.user,
                attend_status__in=['waiting', 'attending']
            ).exists()
        
        return context


@login_required
def add_event_comment(request, event_id):
    """View to add a comment to an event"""
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventCommentForm(request.POST, user=request.user, event=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'There was an error adding your comment.')
    
    return redirect('event-detail-with-comments', pk=event_id)


@login_required
def reply_to_comment(request, comment_id):
    """View to reply to a comment"""
    parent_comment = get_object_or_404(EventComment, id=comment_id)
    
    if request.method == 'POST':
        form = EventCommentForm(request.POST, user=request.user, event=parent_comment.event, parent=parent_comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your reply has been added successfully!')
        else:
            messages.error(request, 'There was an error adding your reply.')
    
    return redirect('event-detail-with-comments', pk=parent_comment.event.id)


class UserMessagesView(LoginRequiredMixin, ListView):
    """View for users to see their sent messages"""
    model = AdminMessage
    template_name = 'events/user_messages.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        return AdminMessage.objects.filter(sender=self.request.user)
