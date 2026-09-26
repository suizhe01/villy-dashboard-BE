"""Progress of an upload, reported while a posting endpoint saves its lines.

The upload page sends a random job key with a posting request (?job=...) and
polls import_progress for it while the request runs. Posting endpoints opt in
with two changes and nothing else:

    @api_view(['POST'])
    @track_import
    def post_x(request):
        ...
        for item in track(data):

Neither may change what an upload saves:
- Without ?job= the decorator calls the view directly and track() passes the
  items straight through, so a request with no job touches no extra table.
- track() yields every item unchanged and in order; it only counts them.
- Every progress write runs in its own savepoint and is caught and logged, so
  a failure to record progress never stops or alters the upload itself, even
  inside a caller's transaction.

Writes go through the IMPORT_PROGRESS_DB database alias ('default' unless
settings say otherwise). The posting views run in autocommit, so each count
is visible to the page as soon as it is written.
"""
import logging
import re
import threading
import time
from datetime import datetime
from functools import wraps

from django.conf import settings
from django.db import transaction

logger = logging.getLogger(__name__)

# How often, at most, the running count is written while lines are saved.
SAVE_INTERVAL_SECONDS = 1.0

_JOB_KEY = re.compile(r'^[A-Za-z0-9_-]{8,40}$')
_current = threading.local()


def _progress_db():
    return getattr(settings, 'IMPORT_PROGRESS_DB', 'default')


def _write(job_key, **fields):
    """Update the job row; never raises."""
    try:
        from importjob.models import ImportJob
        fields['updated_at'] = datetime.now()
        # Its own savepoint: if the write fails inside a caller's transaction,
        # only the savepoint rolls back and the caller's transaction stays
        # usable. Outside a transaction it commits straight away.
        with transaction.atomic(using=_progress_db()):
            ImportJob.objects.using(_progress_db()).filter(job_key=job_key).update(**fields)
    except Exception:
        logger.exception('Could not record upload progress for job %s', job_key)


def _job_key(request):
    try:
        key = request.query_params.get('job')
    except Exception:
        return None
    # A malformed key is ignored: the upload then runs untracked, as today.
    return key if key and _JOB_KEY.match(key) else None


def track_import(view):
    """Record a posting request's progress when it carries ?job=<key>."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        job_key = _job_key(request)
        if job_key is None:
            return view(request, *args, **kwargs)

        try:
            total = len(request.data) if isinstance(request.data, list) else 0
        except Exception:
            # The view reads request.data itself and fails exactly as it would
            # have without tracking.
            total = 0

        try:
            from importjob.models import ImportJob
            now = datetime.now()
            with transaction.atomic(using=_progress_db()):
                ImportJob.objects.using(_progress_db()).create(
                    job_key=job_key, endpoint=view.__name__, total=total, processed=0,
                    status=ImportJob.RUNNING, started_at=now, updated_at=now,
                )
        except Exception:
            logger.exception('Could not start upload progress for job %s', job_key)
            return view(request, *args, **kwargs)

        state = {'key': job_key, 'processed': 0, 'saved_at': time.monotonic()}
        _current.job = state
        try:
            response = view(request, *args, **kwargs)
        except Exception as e:
            _write(job_key, status='failed', processed=state['processed'],
                   finished_at=datetime.now(), error=f'{type(e).__name__}: {e}'[:2000])
            raise
        finally:
            _current.job = None

        status_code = getattr(response, 'status_code', 200)
        if status_code >= 400:
            _write(job_key, status='failed', processed=state['processed'],
                   finished_at=datetime.now(), error=f'HTTP {status_code}')
        else:
            _write(job_key, status='done', processed=state['processed'], finished_at=datetime.now())
        return response
    return wrapper


def track(iterable):
    """Yield each item unchanged, counting it once the loop body has finished."""
    state = getattr(_current, 'job', None)
    if state is None:
        yield from iterable
        return

    for item in iterable:
        yield item
        state['processed'] += 1
        if time.monotonic() - state['saved_at'] >= SAVE_INTERVAL_SECONDS:
            state['saved_at'] = time.monotonic()
            _write(state['key'], processed=state['processed'])
