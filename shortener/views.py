from django.shortcuts import render, redirect, get_object_or_404
from .models import Link

def index(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        link, created = Link.objects.get_or_create(original_url=url)
        if created:
            link.short_code = Link.generate_code()
            link.save()
        return render(request, 'shortener/index.html', {'link': link})
    return render(request, 'shortener/index.html')

def redirect_url(request, code):
    link = get_object_or_404(Link, short_code=code)
    return redirect(link.original_url)
