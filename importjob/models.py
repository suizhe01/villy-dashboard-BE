from django.db import models


class ImportJob(models.Model):
    """Progress of one upload posting request, for the upload page's progress bar.

    The page sends a random job_key with the request (?job=...) and polls this
    row while the server saves the lines. Rows stay as a history of uploads.
    """
    RUNNING = 'running'
    DONE = 'done'
    FAILED = 'failed'
    STATUS_CHOICES = [
        (RUNNING, 'Running'),
        (DONE, 'Done'),
        (FAILED, 'Failed'),
    ]

    job_key = models.CharField(max_length=40, unique=True)
    endpoint = models.CharField(max_length=80)
    total = models.IntegerField(default=0)
    processed = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=RUNNING)
    started_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = "importjob"
