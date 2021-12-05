from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import Authors_Group
from django.shortcuts import render
from django.core import serializers

def prova(request):
    '''
        Vista di prova
    '''
    if(request.user.is_authenticated):
        groups = Authors_Group.objects.filter(user=request.user).order_by('-creation')
        context = {'groups_list': groups}
        #return render(request, 'gbliometrics/groups.html', context)
        data = serializers.serialize('json', groups)
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseBadRequest("Non ti sei loggato")