import sys
import os
import importlib
import logging
from django.apps import AppConfig
from django.conf import settings

logger = logging.getLogger(__name__)

MODULE_NAME = "core"

this = sys.modules[MODULE_NAME]

DEFAULT_CFG = {
    "auto_provisioning_user_group": "user",
    "calendar_package": "core",
    "calendar_module": ".calendars.ad_calendar",
    "datetime_package": "core",
    "datetime_module": ".datetimes.ad_datetime",
    "shortstrfdate": "%d/%m/%Y",
    "longstrfdate": "%a %d %B %Y",
    "iso_raw_date": "False",
    "age_of_majority": "18",
    "async_mutations": "False",
    "currency": "$",
}


class CoreConfig(AppConfig):
    name = MODULE_NAME
    age_of_majority = 18

    def _import_module(self, cfg, k):
        logger.info('import %s.%s' %
                    (cfg["%s_module" % k], cfg["%s_package" % k]))
        return importlib.import_module(
            cfg["%s_module" % k], package=cfg["%s_package" % k])

    def _configure_calendar(self, cfg):
        this.shortstrfdate = cfg["shortstrfdate"]
        this.longstrfdate = cfg["longstrfdate"]
        this.iso_raw_date = False if cfg["iso_raw_date"] is None else cfg["iso_raw_date"].lower(
        ) == "true"
        try:
            this.calendar = self._import_module(cfg, "calendar")
            this.datetime = self._import_module(cfg, "datetime")
        except Exception:
            logger.error('Failed to configure calendar, using default!\n%s: %s' % (
                sys.exc_info()[0].__name__, sys.exc_info()[1]))
            this.calendar = self._import_module(DEFAULT_CFG, "calendar")
            this.datetime = self._import_module(DEFAULT_CFG, "datetime")

    def _configure_majority(self, cfg):
        this.age_of_majority = int(cfg["age_of_majority"])

    def _configure_currency(self, cfg):
        this.currency = str(cfg["currency"])

    def _configure_auto_provisioning(self, cfg):
        if bool(os.environ.get('NO_DATABASE', False)):
            logger.info('env NO_DATABASE set to True: no user auto provisioning possible!')
            return
        group = cfg["auto_provisioning_user_group"]
        this.auto_provisioning_user_group = group
        try:
            from .models import Group
            Group.objects.get(name=group)
        except Group.DoesNotExist:
            g = Group(name=group)
            g.save()
            from django.contrib.auth.models import Permission
            p = Permission.objects.get(codename="view_user")
            g.permissions.add(p)
            g.save()
        except Exception as e:
            logger.warning('Failed set auto_provisioning_user_group '+str(e))

    def _configure_graphql(self, cfg):
        this.async_mutations = True if cfg["async_mutations"] is None else cfg["async_mutations"].lower() == "true"

    def ready(self):
        from .models import ModuleConfiguration
        cfg = ModuleConfiguration.get_or_default(MODULE_NAME, DEFAULT_CFG)
        self._configure_calendar(cfg)
        self._configure_majority(cfg)
        self._configure_auto_provisioning(cfg)
        self._configure_graphql(cfg)
        self._configure_currency(cfg)

        # The scheduler starts as soon as it gets a job, which could be before Django is ready, so we enable it here
        from core import scheduler
        if settings.SCHEDULER_AUTOSTART:
            scheduler.start()
