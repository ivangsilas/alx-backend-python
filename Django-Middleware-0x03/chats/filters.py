# chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="sent_at", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="sent_at", lookup_expr="lte")
    sender_id = django_filters.UUIDFilter(field_name="sender__user_id")

    class Meta:
        model = Message
        fields = ['sender_id', 'start_date', 'end_date']
