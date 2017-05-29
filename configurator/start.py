from django.conf import settings
from django.utils.module_loading import import_string
import logging

from configurator.apps.resource.models import Resource

logger = logging.getLogger(__name__)


def start():
    # prepare environment
    env = {}
    for hook in settings.START_PRE_HOOKS:
        import_string(hook)(env)

    visited = set()
    for resource in Resource.objects.all():
        path = []
        start_single(path, visited, env, resource)

    for hook in settings.START_POST_HOOKS:
        import_string(hook)(env)

    # all entries in environment should be deleted by post-hooks
    if len(env) != 0:
        logger.warning('Not all entries was consumed from the environment. (Left {}.)'.format(len(env)))

def start_single(path, visited, env, resource):
    if resource.id not in visited:

        if resource.id in path:
            raise Exception('Dependency cycle detected: {}'.format(path))

        path.append(resource.id)
        for requirement in resource.requirements:
            start_single(path, visited, env, requirement)
        resource.start(env)
        assert path.pop() == resource.id

        visited.add(resource.id)
