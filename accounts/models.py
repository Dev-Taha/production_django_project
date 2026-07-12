from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True, unique=True)
    password = models.CharField(max_length=255, null=True)
    google_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    profile_picture = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # Required for Django's auth system check when AUTH_USER_MODEL is set
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    is_anonymous = False
    is_authenticated = True

    @property
    def is_google_user(self):
        return self.google_id is not None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    