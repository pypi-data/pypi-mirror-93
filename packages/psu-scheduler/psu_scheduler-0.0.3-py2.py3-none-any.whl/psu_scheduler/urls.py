from django.urls import path
from . import views

urlpatterns = [
    # Run Scheduled Jobs
    path('run', views.run_jobs, name='run_jobs'),

    # A sample/test job
    path('test', views.test_job, name='test_job'),

    # Manage Schedules
    path('list', views.job_list, name='jobs'),
    path('save', views.save_job, name='save_job'),

    # Manage Jobs
    path('endpoint/list', views.endpoint_list, name='endpoints'),
    path('endpoint/save', views.save_endpoint, name='save_endpoint'),

    # View scheduled job executions
    path('endpoint/executions', views.executions, name='executions'),
]
