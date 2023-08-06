from psu_base.classes.Log import Log
from psu_base.context_processors import util as util_context
from psu_base.services import utility_service, error_service
from psu_scheduler.models import ScheduledJob, JobExecution, EndpointDefinition
from collections import OrderedDict

log = Log()


def get_jobs_to_run():
    """
    Check each defined job to see if it needs to run
    """
    log.trace()
    jobs = ScheduledJob.objects.all()
    run_list = []
    if jobs:
        for jj in jobs:
            if jj.should_run():
                run_list.append(jj)
    return run_list


def get_absolute_url(job_url):
    context = util_context(utility_service.get_request())
    return f"{context['absolute_root_url']}{job_url}"


def get_endpoint_options():
    options = utility_service.recall()
    if options:
        return options

    log.trace()
    options = OrderedDict()
    try:
        eps = EndpointDefinition.objects.filter(app_code=utility_service.get_app_code()).order_by('title')
        for ep in eps:
            options[ep.id] = ep.title

    except Exception as ee:
        error_service.unexpected_error(
            "Unable to retrieve schedule-able jobs", ee
        )

    return utility_service.store(options)
