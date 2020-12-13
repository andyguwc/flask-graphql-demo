# -*- coding: utf-8 -*-
import graphene
from graphene import relay
from graphene_sqlalchemy import (SQLAlchemyConnectionField,
                                 SQLAlchemyObjectType)
from demo.models import User as UserModel
from demo.models import Post as PostModel
from demo.extensions import db

class User(SQLAlchemyObjectType):
    """Users"""
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )


class Post(SQLAlchemyObjectType):
    """Posts"""
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )


class CreateUser(graphene.Mutation):
    """Create user"""
    class Arguments:
        username = graphene.String()
        email = graphene.String()
    
    user = graphene.Field(User)
    ok = graphene.Boolean()

    def mutate(self, info, username, email):
        user = UserModel(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return CreateUser(user=user, ok=True)


class Query(graphene.ObjectType):
    """Query endpoint for GraphQL API"""
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User.connection)
    all_posts = SQLAlchemyConnectionField(Post.connection)
    user = relay.Node.Field(User)
    post = relay.Node.Field(Post)


class Mutation(graphene.ObjectType):
    """Mutation endpoint for GraphQL API"""
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
