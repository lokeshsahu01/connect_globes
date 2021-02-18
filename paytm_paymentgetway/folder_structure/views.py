from django.shortcuts import render


def folder_view(request):
    return render(request, 'folder.html')
