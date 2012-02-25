from django.shortcuts import render_to_response

def index(request):
    '''Render a fancy static frontpage.
    '''
    return render_to_response('index.html')
