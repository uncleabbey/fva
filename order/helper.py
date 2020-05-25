from .models import MessageStatus, Notification


def send_notification(subjectUser, orderId, message):
    message_status = MessageStatus.objects.create(name='S')
    notification = Notification.objects.create(
        subjectUser=subjectUser,
        orderId=orderId,
        message=message,
        messageStatus=message_status
    )
    return notification


def get_status(status):
    if status == 'D':
        return ' has been Delivered'
    elif status == 'T':
        return ' is In-Transit'
    elif status == 'C':
        return ' has been Canceled'
    else:
        return ' is been Proccesing'
