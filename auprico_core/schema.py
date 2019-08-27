import graphene
from graphene import Node
from graphene_django import DjangoObjectType

from auprico_core.models import Country


class CountableConnectionBase(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        try:
            return self.iterable.paginator.count
        except:
            return self.length


class CountryNode(DjangoObjectType):
    class Meta:
        model = Country
        interfaces = (Node,)
        filter_fields = []
        connection_class = CountableConnectionBase


