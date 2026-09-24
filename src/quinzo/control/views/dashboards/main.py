from django.shortcuts import render

def main_dashboard(request):
    ctx = {}
    return render(request, 'quinzocontrol/dashboard.html', ctx)
    