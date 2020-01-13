from .models import NotificationItem


MAX_NOTIF = 3


# function that pulls the last MAX_NOTIF notifications and returns them
# as a dictionary
def pull_notif(t_user):
    all_ordered = NotificationItem.objects.filter(user__id=t_user.id).order_by('-created_at')
    index_max = min(len(all_ordered), MAX_NOTIF)

    has_unread = False

    for x in all_ordered[:index_max]:
        if x.read == False:
            has_unread = True
            break

    return [has_unread, all_ordered[:index_max]]


# function that marks last MAX_NOTIF as read
def mark_read(t_user):
    all_ordered = NotificationItem.objects.filter(user__id=t_user.id).order_by('-created_at')
    index_max = min(len(all_ordered), MAX_NOTIF)

    for x in all_ordered[:index_max]:
        x.read = True
        x.save()

    return