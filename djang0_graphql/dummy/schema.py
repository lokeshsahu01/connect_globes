from graphene_django import DjangoObjectType
import graphene
from .models import *


class UserModelType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = ('id', 'name', 'last_name')


class Query(graphene.ObjectType):
    users = graphene.List(UserModelType)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()


schema = graphene.Schema(query=Query)

