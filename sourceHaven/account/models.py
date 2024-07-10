from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify
from django.contrib.auth import get_user_model


class Profile(models.Model):
    ADMIN_STATUS_CHOICES = {
        'AD': 'ADMIN',
        'MD': 'MODERATOR',
        'US': 'USER',
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/')
    is_active = models.BooleanField(default=True)
    profile_status = models.CharField(max_length=150)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    admin_status = models.CharField(max_length=2, choices=ADMIN_STATUS_CHOICES.items(), default='US')
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['profile_name'])
        ]

    def __str__(self):
        return f"Профиль {self.profile_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.profile_name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('account:profile_detail', args=[self.slug])


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='from_user')
    user_to = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='to_user')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


User = get_user_model()
User.add_to_class('contact_from', models.ManyToManyField('self', through=Contact, symmetrical=False, related_name='contact_to'))
