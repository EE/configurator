from django.db import models
from configurator.apps.resource.models import Resource
import psycopg2
import psycopg2.sql
import secrets


class PostgreSQLServer(models.Model):
    """Location and admin access to a PostgreSQL server."""
    host = models.CharField(max_length=200)
    port = models.IntegerField()
    admin_user = models.CharField(max_length=200)
    admin_password = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('host', 'port')

    def connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.admin_user,
            password=self.admin_password
        )

    def __str__(self):
        return 'PostgreSQL server {}:{}'.format(self.host, self.port)


class PostgreSQLDatabaseAccess(Resource):
    """Access to a PostgreSQL database."""
    type_name = 'postgresql'

    server = models.ForeignKey(PostgreSQLServer)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200, default=secrets.token_urlsafe)
    database = models.CharField(max_length=200)

    class Meta:
        unique_together = (
            ('server', 'user'),
            ('server', 'database'),
        )

    def save(self, *args, **kwargs):
        if not self.database:
            self.database = self.user
        return super().save(*args, **kwargs)

    @property
    def requirements(self):
        return frozenset()

    @property
    def optional_requirements(self):
        return frozenset()

    def to_rendering_context(self):
        return {
            'user': self.user,
            'password': self.password,
            'database': self.database,
            'host': self.server.host,
            'port': self.server.port,
        }

    def start(self, env):
        with self.server.connection() as conn:

            # disable transactions - CREATE DATABASE needs to run
            #   outside a transaction. In the worst case scenario user
            #   or db will be created many times causing all executing
            #   programs except first one to crash.
            conn.autocommit = True

            user_identifier = psycopg2.sql.Identifier(self.user).as_string(conn)
            database_identifier = psycopg2.sql.Identifier(self.database).as_string(conn)

            with conn.cursor() as cur:

                # create user if one doesnt exist
                cur.execute('SELECT count(*) FROM pg_roles WHERE rolname = %s', (self.user,))
                if cur.fetchone() == (0,):
                    cur.execute('CREATE ROLE {}'.format(user_identifier))

                # update user settings
                cur.execute(
                    'ALTER ROLE {} PASSWORD %s LOGIN'.format(user_identifier),
                    (self.password,)
                )

                # create database if one doesnt exist
                cur.execute('SELECT count(*) FROM pg_database WHERE datname = %s', (self.database,))
                if cur.fetchone() == (0,):
                    cur.execute('CREATE DATABASE {}'.format(database_identifier))

                # update db settings
                cur.execute('ALTER DATABASE {} OWNER TO {}'.format(database_identifier, user_identifier))

            conn.commit()

    def __str__(self):
        return 'PostgreSQL database access {}@{}:{}/{}'.format(
            self.user, self.server.host, self.server.port, self.database)
