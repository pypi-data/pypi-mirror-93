import datetime

from . import models
from .util.helpers import get_object_from_arg
from typing import Optional


def get_subjects(offset: Optional[int]=None,
                 limit: Optional[int]=None,
                 order: Optional[str]=None):
    query = models.Subject.query
    count = query.count()

    if order == 'asc':
        query = query.order_by(models.Subject.id.asc())
    elif order == 'desc':
        query = query.order_by(models.Subject.id.desc())

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    subjects = query.all()

    return subjects, count


def get_experiments(subject: Optional[str]=None,
                    scandate: Optional[datetime.datetime]=None,
                    state: Optional[str]=None,
                    offset: Optional[int]=None,
                    limit: Optional[int]=None,
                    order: Optional[str]=None):
    query = models.Experiment.query

    if subject is not None:
        query = query.filter(models.Experiment.subject_id == subject)

    if scandate is not None:
        query = query.filter(models.Experiment.scandate == scandate)

    if order == 'asc':
        query = query.order_by(models.Experiment.id.asc())
    elif order == 'desc':
        query = query.order_by(models.Experiment.id.desc())

    # This should move to the DB if possible, but querying on state is problematic
    if state is not None:
        state = get_object_from_arg(state, models.State, models.State.label)
        experiments = query.all()
        experiments = [x for x in experiments if x.state == state]

        # Do limit and offset post-hoc, as we can't use the DB for that
        count = len(experiments)
        if offset:
            experiments = experiments[offset:]

        if limit:
            experiments = experiments[:limit]
    else:
        # Count is safe as there shouldn't be duplicates possible in this list
        count = query.count()

        # Add limit and offset to query
        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        experiments = query.all()

    return experiments, count
