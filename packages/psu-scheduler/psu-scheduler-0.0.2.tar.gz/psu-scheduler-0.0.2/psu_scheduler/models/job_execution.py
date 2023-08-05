from django.db import models
from psu_base.classes.Log import Log
from .scheduled_job import ScheduledJob
log = Log()


class JobExecution(models.Model):
    """Record of a scheduled task being performed"""

    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(auto_now=True)

    job = models.ForeignKey(ScheduledJob, models.CASCADE, blank=False, null=False, db_index=True)
    key = models.CharField(
        max_length=20,
        blank=False, null=False,
        db_index=True
    )
    status = models.CharField(
        max_length=30,
        blank=False, null=False, default="init"
    )
    output = models.TextField(blank=True, null=True)

    def started_at(self):
        return f"{self.date_created.hour}{self.date_created.minute}"

    def status_description(self):
        if self.status == 'init':
            return "Initialized"
        elif self.status == 'run':
            return 'Running'
        elif self.status == 'done':
            return 'Completed'
        else:
            return self.status

    @classmethod
    def get(cls, je_id):
        try:
            return JobExecution.objects.get(pk=je_id)
        except JobExecution.DoesNotExist:
            return None
