from psu_base.classes.Log import Log
from functools import wraps
from django.http import HttpResponseForbidden
from psu_scheduler.models import JobExecution
from psu_base.services import auth_service

log = Log()


def scheduled_job():
    """
    Decorator for views that are executed as scheduled jobs
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            exe = None
            allowed = False

            # If the job ID and Key provided?
            if 'job_key' in request.GET and 'job_id' in request.GET:
                job_id = request.GET.get('job_id')
                job_key = request.GET.get('job_key')

                # Get the job execution record
                exe = JobExecution.get(job_id)
                # If not found, invalid key, or already ran - Log a message
                if not exe:
                    log.error(f"Scheduled job #{job_id} does not exist")
                elif exe.key != job_key:
                    log.error(f"Incorrect key for scheduled job #{job_id}: {job_key}")
                elif exe.status != 'init':
                    log.error(f"Scheduled job #{job_id} already ran")
                else:
                    log.info(f"Scheduled job #{job_id} is allowed to run")
                    allowed = True

            elif auth_service.has_authority('DynamicSuperUser'):
                log.info(f"SuperUser {auth_service.get_user().display_name} is allowed to run scheduled jobs")
                allowed = True

            else:
                log.error(f"Scheduled job was called without providing an ID and Key")

            # Return Forbidden response if not allowed
            if not allowed:
                return HttpResponseForbidden('Job was not allowed to run')

            # Otherwise, render the view
            elif exe:
                exe.status = 'running'
                exe.save()

                if exe.job.performer:
                    # ToDo: Fake authentication for performer, if specified
                    pass

                return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
