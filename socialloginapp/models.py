import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models, validators as auth_validators
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SocialLoginAppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
  objects = auth_models.UserManager()
  username_validator = auth_validators.UnicodeUsernameValidator()
  EMAIL_FIELD = "email"
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username"]
  username = models.CharField(
      _("username"),
      max_length=150,
      unique=False,
      help_text=_(
          "Not Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
      ),
      validators=[username_validator],
      error_messages={"unique": _("A user with that username already exists.")},
  )
  # guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  picture = models.ImageField(blank=True, upload_to=settings.MEDIA_ROOT)

  email = models.EmailField(_("email address"), unique=True)
  first_name = models.EmailField(
      _("first name"), max_length=1024, blank=False, null=True
  )
  last_name = models.CharField(
      _("last name"), max_length=1024, blank=False, null=True
  )
  is_staff = models.BooleanField(
    _('staff status'),
    default=False,
    help_text=_('Designates whether the user can log into this admin site.'),
  )
  is_active = models.BooleanField(
    _('active'),
    default=True,
    help_text=_(
      'Designates whether this user should be treated as active. '
      'Unselect this instead of deleting accounts.'
    ),
  )
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

