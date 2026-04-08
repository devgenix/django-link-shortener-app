from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Link

def index(request):
    links = Link.objects.all()[:5]
    if request.method == 'POST':
        url = request.POST.get('url')
        if not url:
            messages.error(request, "Please provide a valid URL.")
            return render(request, 'shortener/index.html', {'links': links})
        
        link, created = Link.objects.get_or_create(original_url=url)
        if created:
            link.short_code = Link.generate_code()
            link.save()
            messages.success(request, "Link shortened successfully!")
        
        return render(request, 'shortener/index.html', {
            'link': link,
            'short_url': request.build_absolute_uri('/') + link.short_code,
            'links': links
        })
    return render(request, 'shortener/index.html', {'links': links})

def redirect_url(request, code):
    link = get_object_or_404(Link, short_code=code)
    link.clicks += 1
    link.save()
    return redirect(link.original_url)
