import io
import requests
import typing

from django.conf import settings
from django.core.files import File
from django.contrib.auth import login

def user_picture(strategy, details: typing.Dict[str, typing.Any], user=None, *args, **kwargs) -> None:
  try:
    picture_url: str = kwargs['response']['picture']['data']['url']
  except KeyError:
    picture_url: str = None

  else:
    stream = requests.get(picture_url, headers=settings.SOCIAL_AUTH_HEADERS, stream=True)
    _file = io.BytesIO()
    for chunk in stream.iter_content(chunk_size=1024):
      _file.write(chunk)
  
    _file.seek(0)
    user = strategy.get_user()
    user.picture.save('profile-pic', File(_file, name='profile-pic'))
    user.save()

def user_login(strategy, details: typing.Dict[str, typing.Any], user=None, *args, **kwargs) -> None:
  login(kwargs['request'], strategy.get_user(), backend='social_core.backends.facebook.FacebookOAuth2')

