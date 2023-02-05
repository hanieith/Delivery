from django.shortcuts import render


def home(request):
    return render(request, template_name='dostavka/index.html', context={'title': 'Home'})
