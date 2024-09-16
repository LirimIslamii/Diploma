from django.views import View
from django.http import JsonResponse
import threading
import uuid
import logging
from django.views.generic import TemplateView

# Configure logging
logger = logging.getLogger(__name__)

# Global dictionary to store training progress
TRAINING_PROGRESS = {}
TRAINING_PROGRESS_LOCK = threading.Lock()

class GetTrainingProgressView(TemplateView):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id')
        if not task_id:
            return JsonResponse({'error': 'No task_id provided'}, status=400)
        
        with TRAINING_PROGRESS_LOCK:
            progress = TRAINING_PROGRESS.get(task_id, {'error': 'No progress available.'})
        
        return JsonResponse(progress)