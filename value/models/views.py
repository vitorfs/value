from django.shortcuts import render

def models(request):
    return render(request, 'models/models.html')

def model(request, model_id):
    return render(request, 'models/model.html')
