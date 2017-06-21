from django.db import models
from polymorphic.models import PolymorphicModel
from importlib import import_module


class Resource(PolymorphicModel):
    """Abstract resource.

    Subclasses should define class variables:
     * serializer_name = ('path.to.module', 'SerializerClassName')
    """

    @classmethod
    def serializer(cls):
        """Serializer for this class retrieveved from class variable
        `serializer_name`."""
        return getattr(
            import_module(cls.serializer_name[0]),
            cls.serializer_name[1]
        )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    @property
    def requirements(self):
        """Frozenset of resources directly required by this resource."""
        raise NotImplementedError()

    @property
    def optional_requirements(self):
        """Frozenset of resources directly optionally required by this
        resource."""
        raise NotImplementedError()

    def to_rendering_context(self):
        """Convert resource to structure of dicts and lists suitable for
        feeding into renderer (jinja) as a context."""
        raise NotImplementedError()

    def flatten(self):
        """Frozenset of resources with skipped resources that are
        "empty" - like lists and dicts."""
        return frozenset([self])

    def start(self, env):
        """Start resource in given environment."""
        pass

    def __str__(self):
        return self.name


class StringResource(Resource):
    serializer_name = ('configurator.apps.resource.serializers', 'StringSerializer')

    value = models.TextField()

    @property
    def requirements(self):
        return frozenset()

    @property
    def optional_requirements(self):
        return frozenset()

    def to_rendering_context(self):
        return self.value

    def __str__(self):
        return (self.value[:20] + "..") if len(self.value) > 20 else self.value


class IntResource(Resource):
    serializer_name = ('configurator.apps.resource.serializers', 'IntSerializer')

    value = models.IntegerField()

    @property
    def requirements(self):
        return frozenset()

    @property
    def optional_requirements(self):
        return frozenset()

    def to_rendering_context(self):
        return self.value

    def __str__(self):
        return "{}".format(self.value)


class ListResource(Resource):
    """List of resources. All of them should be same type."""
    serializer_name = ('configurator.apps.resource.serializers', 'ListSerializer')

    value = models.ManyToManyField(
        Resource, related_name="member_of_lists", blank=True)

    @property
    def requirements(self):
        return frozenset()

    @property
    def optional_requirements(self):
        return frozenset(self.value.all())

    def to_rendering_context(self):
        return [e.to_rendering_context() for e in self.value.all()]

    def flatten(self):
        return frozenset().union(*[r.flatten() for r in self.value.all()])


class DictResource(Resource):
    """Dictionary of which keys are strings and values are resources."""
    serializer_name = ('configurator.apps.resource.serializers', 'DictSerializer')

    @property
    def requirements(self):
        return frozenset(entry.value for entry in self.entries.all())

    @property
    def optional_requirements(self):
        return frozenset()

    def as_dict(self):
        return {entry.key: entry.value for entry in self.entries.all()}

    def to_rendering_context(self):
        return {
            entry.key: entry.value.to_rendering_context()
            for entry in self.entries.all()
        }

    def flatten(self):
        return frozenset().union(*[r.value.flatten() for r in self.entries.all()])


class DictResourceEntry(models.Model):
    """Single mapping string -> resource in dictionary of resources."""
    dictionary = models.ForeignKey(DictResource, related_name="entries")
    key = models.TextField()
    value = models.ForeignKey(Resource)

    def __str__(self):
        return "{}: {}".format(self.key, self.value)
