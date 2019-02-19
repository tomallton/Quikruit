from django.shortcuts import render

# Create your views here.
def global_homepage(request):
	return render(request, 'core/global_homepage.html', None)