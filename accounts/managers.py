from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

from accounts.validators import validate_username


class UserManager(BaseUserManager):
    def generate_username(self, email: str) -> str:
        """Generate username based on `email` field.

        Generate unique username for the database based on `email` field.

        Args:
            email: Email of a user.

        Returns:
            The generated username.

        Raises:
            ValueError: if `email` is empty string or None.
        """

        if not email:
            raise ValueError("Email is empty or None.")

        username = email.split("@")[0]
        validate_username(username)
        if not self.filter(username=username).exists():
            return username
        suffix = 2
        while self.filter(username=username + str(suffix)).exists():
            suffix += 1

        return username + str(suffix)

    def _create_user(
        self,
        email,
        password,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)
        username = extra_fields.get("username")
        if not username or self.filter(username=username).exists():
            full_name = extra_fields.get("full_name", "user")
            extra_fields["username"] = self.generate_username(full_name)
        user = self.model(
            email=email,
            is_active=True,
            date_joined=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user = self._create_user(email, password, **extra_fields)
        user.save(using=self._db)
        return user
