from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_migrate)
def init_superuser(sender, **kwargs):
    User = get_user_model()
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        User.objects.create_superuser('', 'admin@secretdiaryapp.org', '')