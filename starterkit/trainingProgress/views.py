from django.http import JsonResponse

def get_training_progress(request):
    try:
        training_progress = request.session.get('training_progress', {})
        return JsonResponse(training_progress)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
