from django.shortcuts import render

def index(request):
  return render(request, 'socialloginapp/index.html', {
    'user': request.user
  })

# Create your views here.
