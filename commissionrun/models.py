from django.db import models


class CommissionRun(models.Model):
    """One press of Check: a commission calculation for a date range.

    Every page polls the latest row to show who else is calculating, and the
    Cancel button sets cancel_requested, which the pipeline checks between
    steps. Rows are kept as a history of what was recalculated and when.
    """
    RUNNING = 'running'
    DONE = 'done'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (RUNNING, 'Running'),
        (DONE, 'Done'),
        (CANCELLED, 'Cancelled'),
        (FAILED, 'Failed'),
    ]

    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=RUNNING)
    cancel_requested = models.BooleanField(default=False)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    # JSON list of [step name, seconds], showing whether cancel needs finer checks
    step_timings = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "commissionrun"
