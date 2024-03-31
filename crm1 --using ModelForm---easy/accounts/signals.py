from django.db.models.signals  import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from .models import Customer


@receiver(post_save,sender=User)
def create_customer_profile(sender,created,instance,**kwargs):
    if created:
        # once a user is register customer(profile) is automatically created
        Customer.objects.create(user=instance)
        
        # and that customer is also added into the 'customerGroup'
        customer_group =Group.objects.get(name='customerGroup')
        instance.groups.add(customer_group)