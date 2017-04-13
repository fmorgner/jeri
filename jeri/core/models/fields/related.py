from jeri.core.models.fields.base import RelatedField


class OneToManyField(RelatedField):

    def hydrate(self, object, list):
        manager = self.manager(self.to.objects)
        for entry in list:
            manager.add_relation(entry)
        setattr(object, self.name, manager)


class OneToOneField(RelatedField):
    pass
