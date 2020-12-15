# -*- coding: utf-8 -*-
import graphene
from graphene import relay
from graphql import GraphQLError
from graphene_sqlalchemy import (SQLAlchemyConnectionField,
                                 SQLAlchemyObjectType)
from demo.models import User as UserModel
from demo.models import Post as PostModel
from demo.extensions import db
from graphql_relay.node.node import from_global_id


def require_auth(method):
    """Decorator to check auth and populate user"""
    def wrapper(self, *args, **kwargs):
        auth_resp = UserModel.decode_auth_token(args[0].context)
        if not isinstance(auth_resp, str):
            kwargs['user'] = UserModel.query.filter_by(id=auth_resp).first()
            return method(self, *args, **kwargs)
        raise GraphQLError(auth_resp)
    return wrapper


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


class Query(graphene.ObjectType):
    """Query endpoint for GraphQL API"""
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User.connection)
    all_posts = SQLAlchemyConnectionField(Post.connection)

    users_by_username = graphene.List(User, username=graphene.String())
    user = relay.Node.Field(User)
    post = relay.Node.Field(Post)

    @staticmethod
    def resolve_users_by_username(parent, info, **args):
        username = args.get('username')
        return User.get_query(info).filter(UserModel.username == username).all()


class SignUp(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)
    auth_token = graphene.String()

    def mutate(self, info, **kwargs):
        user = UserModel()
        user.from_dict(kwargs, new_user=True)
        db.session.add(user)
        db.session.commit()
        return SignUp(user=user, auth_token=user.encode_auth_token(user.id).decode())


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(User)
    auth_token = graphene.String()

    def mutate(self, info, **kwargs):
        user = UserModel.query.filter_by(username=kwargs.get('username')).first()
        if user is None or not user.verify_password(kwargs.get('password')):
            raise GraphQLError("Invalid Credentials")
        return Login(user=user, auth_token=user.encode_auth_token(user.id).decode())


class CreatePost(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    post = graphene.Field(Post)

    @require_auth
    def mutate(self, info, **kwargs):
        author = UserModel.query.filter_by(id=kwargs.get('author_id')).first()
        if kwargs.get('user') != author:
            raise GraphQLError("You don't have permission to create this post")
        post = PostModel()
        post.from_dict(kwargs, author=author, new_post=True)
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        body = graphene.String()
    
    post = graphene.Field(Post)

    @require_auth
    def mutate(self, info, **kwargs):
        post = PostModel.query.filter_by(id=kwargs.get('id')).first()
        author = UserModel.query.filter_by(id=post.author.id).first()
        if kwargs.get('user') != author:
            raise GraphQLError("You don't have permission to update this post")
        post.from_dict(kwargs, new_post=False)
        db.session.add(post)
        db.session.commit()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
    
    ok = graphene.Boolean()

    @require_auth
    def mutate(self, info, **kwargs):
        post = PostModel.query.filter_by(id=kwargs.get('id')).first()
        author = UserModel.query.filter_by(id=post.author.id).first()
        if kwargs.get('user') != author:
            raise GraphQLError("You don't have permission to update this post")
        db.session.delete(post)
        db.session.commit()
        return DeletePost(ok=True)


class Mutation(graphene.ObjectType):
    """Mutation endpoint for GraphQL API"""
    signup = SignUp.Field()
    login = Login.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
