import typing as t
from unittest import TestCase

from ingots.tests.units.scripts.test_base import BaseDispatcherTestsMixin

from ingot_prometheus.scripts.ingot_prometheus import IngotPrometheusDispatcher

__all__ = ("IngotPrometheusDispatcherTestsMixin",)


class IngotPrometheusDispatcherTestsMixin(BaseDispatcherTestsMixin):
    """Contains tests for the IngotPrometheusDispatcher class and checks it."""

    tst_cls: t.Type = IngotPrometheusDispatcher
    tst_builder_name = "test"


class IngotPrometheusDispatcherTestCase(IngotPrometheusDispatcherTestsMixin, TestCase):
    """Checks the IngotPrometheus class."""
