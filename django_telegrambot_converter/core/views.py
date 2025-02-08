# from django.http import JsonResponse
# from .tasks import task_get_rates_from_api
# from celery.result import AsyncResult
#
#
# def update_rates_and_get_status(request):
#     task = task_get_rates_from_api.delay()
#
#     check_status_task = check_task_status.delay(task.id)
#
#     return JsonResponse({'task_id': task.id, 'check_status_task_id': check_status_task.id})
#
#
# def get_task_status(request, task_id):
#     result = AsyncResult(task_id)
#     return JsonResponse({
#         'task_id': task_id,
#         'status': result.status,
#         'result': result.result
#     })