# -*- coding: utf-8 -*-
import graphene
from graphene import relay
from graphene_sqlalchemy import (SQLAlchemyConnectionField,
                                 SQLAlchemyObjectType)
from demo.models import User as UserModel
from demo.models import Post as PostModel


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Post(SQLAlchemyObjectType):

    class Meta:
        model = PostModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User.connection)
    all_posts = SQLAlchemyConnectionField(Post.connection)


schema = graphene.Schema(query=Query)