from optparse import make_option
import logging

from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps

from django_pgviews.models import ViewSyncer


log = logging.getLogger('django_pgviews.sync_pgviews')


class Command(BaseCommand):
    help = """Create/update Postgres views for all installed apps."""
    
    def add_arguments(self, parser):
        parser.add_argument('--no-update',
            action='store_false',
            dest='update',
            default=True,
            help="""Don't update existing views, only create new ones.""")
        parser.add_argument('--force',
            action='store_true',
            dest='force',
            default=False,
            help="""Force replacement of pre-existing views where
            breaking changes have been made to the schema.""")
        parser.add_argument('--include_materialized_views',
            action='store_true',
            dest='include_materialized_views',
            default=False,
            help="""Include materialized views on the sync process.
            They are not included by default.""")

    def handle(self, force, update, include_materialized_views, **options):
        vs = ViewSyncer()
        vs.run(force, update, include_materialized_views)
