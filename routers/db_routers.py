from django_celery_beat.schedulers import DatabaseScheduler
from django.db import transaction, close_old_connections
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DatabaseError
from celery.utils.log import get_logger

logger = get_logger(__name__)
debug, info, warning = logger.debug, logger.info, logger.warning

class FoodRouter:
    route_app_labels = {'collection'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'food'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'food'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        # if (
        #     obj1._meta.app_label in self.route_app_labels or
        #     obj2._meta.app_label in self.route_app_labels
        # ):
        db_set = {'food', 'ml'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == 'food':
            return app_label in self.route_app_labels # don't allow django_* tables

        if app_label in self.route_app_labels:
            return db == 'food'
        return None 

class MLRouter:
    route_app_labels = {'admin', 'auth', 'contenttypes', 'labeling', 'djcelery', 'celery', 'django_celery_results', 'sessions', 'tasks', 'django_celery_beat', 'taggit', 'celery.backend_cleanup'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'ml'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'ml'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # if (
        #     obj1._meta.app_label in self.route_app_labels or
        #     obj2._meta.app_label in self.route_app_labels
        # ):
        db_set = {'food', 'ml'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'ml'
        return False

    def allow_syncdb(self, db, model):
        if db == 'ml':
            # Only put models from APPS into Celery table (and south for
            # migrations).
            return model._meta.app_label in self.route_app_labels + ('south',)
        elif model._meta.app_label in self.route_app_labels:
            # Don't put Celery models anywhere else.
            return False
        return None


class MLDatabaseScheduler(DatabaseScheduler):

    def sync(self):
        info('Writing entries...')
        _tried = set()
        db = 'ml'
        try:
            close_old_connections()
            with transaction.atomic(using=db):
                while self._dirty:
                    try:
                        name = self._dirty.pop()
                        _tried.add(name)
                        self.schedule[name].save()
                    except (KeyError, ObjectDoesNotExist):
                        pass
        except DatabaseError as exc:
            # retry later
            self._dirty |= _tried
            logger.exception('Database error while sync: %r', exc)

    def schedule_changed(self):
        try:
            # If MySQL is running with transaction isolation level
            # REPEATABLE-READ (default), then we won't see changes done by
            # other transactions until the current transaction is
            # committed (Issue #41).
            db = 'ml'
            try:
                transaction.commit(using=db)
            except transaction.TransactionManagementError:
                pass  # not in transaction management.

            last, ts = self._last_timestamp, self.Changes.last_change()
        except DatabaseError as exc:
            logger.exception('Database gave error: %r', exc)
            return False
        try:
            if ts and ts > (last if last else ts):
                return True
        finally:
            self._last_timestamp = ts
        return False

