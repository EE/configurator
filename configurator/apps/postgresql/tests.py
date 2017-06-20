from django.core.exceptions import ValidationError
from django.test import TestCase
import testing.postgresql
from .models import *
import psycopg2


class PostgreSQLServerIntegrationTest(TestCase):

    def setUp(self):
        self.postgresql = testing.postgresql.Postgresql()
        self.properties = self.postgresql.dsn()

        self.server = PostgreSQLServer.objects.create(
            host=self.properties['host'],
            port=self.properties['port'],
            admin_user=self.properties['user']
        )

        self.access = PostgreSQLDatabaseAccess.objects.create(
            server=self.server,
            user='aaaa',
            password='aaaa_very_secret',
            database='aaaa_db'
        )

    def tearDown(self):
        self.postgresql.stop()

    def log_in(self):
        with psycopg2.connect(
            host=self.properties['host'],
            port=self.properties['port'],
            user='aaaa',
            password='aaaa_very_secret',
            dbname='aaaa_db'
        ) as conn:
            pass

    def test_create_user(self):
        # role can't log in
        with self.assertRaises(psycopg2.OperationalError):
            self.log_in()

        # after starting resource role can log in
        self.access.start(None)
        self.log_in()

        # after starting for the second time role can still log in
        self.access.start(None)
        self.log_in()


class PostgreSQLDatabaseAccessTest(TestCase):

    def setUp(self):
        self.server = PostgreSQLServer.objects.create(
            host='host.name',
            port=5,
            admin_user='admin'
        )

    def test_defaults(self):
        a = PostgreSQLDatabaseAccess.objects.create(
            server=self.server,
            user='aaaa',
        )
        self.assertGreater(len(a.password), 10)
        self.assertEqual(a.database, 'aaaa')

    def test_uniqueness(self):
        PostgreSQLDatabaseAccess.objects.create(
            server=self.server,
            user='aaaa',
            database='bbbb'
        )
        with self.assertRaises(ValidationError):
            PostgreSQLDatabaseAccess.objects.create(
                server=self.server,
                user='aaaa',
                database='cccc'
            ).full_clean()
        with self.assertRaises(ValidationError):
            PostgreSQLDatabaseAccess.objects.create(
                server=self.server,
                user='cccc',
                database='bbbb'
            ).full_clean()
