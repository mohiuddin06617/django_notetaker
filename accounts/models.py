from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone

from accounts.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """The main model for an account.

    Fields:
        email: Creation of a user happens after email authentication, so the
            `email` field is unique for users.
        full_name: Store the full name of a user.
        username: Generates based on `first_name`.
        ...
    """

    email = models.EmailField(
        "Email",
        max_length=254,
        unique=True,
        blank=False,
        db_index=True,
        null=False,
    )
    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
        blank=True,
        null=False,
        help_text="Username should include only Latin letters, digits, and dots. "
        "Username can't start and end with a dot or don't contain letters. "
        "Digits can be added only at the end.",
        validators=[UnicodeUsernameValidator()],
    )
    full_name = models.CharField(
        "Full Name",
        max_length=50,  # Adjust the max length as needed
        blank=True,
        help_text="Your name appears around NoteD where you post or do actions.",
    )
    is_staff = models.BooleanField("Staff", default=False)
    is_superuser = models.BooleanField("Superuser", default=False)
    is_active = models.BooleanField("User activated", default=True)
    last_login = models.DateTimeField("Last Login", null=True, blank=True)
    date_joined = models.DateTimeField("Date Joined", default=timezone.now)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="accounts_user_groups",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="accounts_user_permissions",
        blank=True,
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self._state.adding and (
            not self.username
            or User.objects.filter(username=self.username).exists()
        ):
            self.username = User.objects.generate_username(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"
