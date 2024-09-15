from django.http import JsonResponse

def get_training_progress(request):
    training_progress = request.session.get('training_progress', {
        'epoch': 0,
        'loss': 'n/a',
        'accuracy': 'n/a',
        'val_loss': 'n/a',
        'val_accuracy': 'n/a'
    })
    return JsonResponse(training_progress)
