# -*- coding: utf-8 -*-
import graphene
# from graphene import relay
from graphql import GraphQLError
from graphene_sqlalchemy import (SQLAlchemyConnectionField,
                                 SQLAlchemyObjectType)
from demo.models import User as UserModel
from demo.models import Post as PostModel
from demo.models import Vote as VoteModel

from demo.extensions import db
# from graphql_relay.node.node import from_global_id


def require_auth(method):
    """Decorator to check auth and populate user"""
    def wrapper(self, *args, **kwargs):
        auth_resp = UserModel.decode_auth_token(args[0].context)
        if not isinstance(auth_resp, str):
            kwargs['user'] = UserModel.query.filter_by(id=auth_resp).first()
            return method(self, *args, **kwargs)
        raise GraphQLError(auth_resp)
    return wrapper


class CustomNode(graphene.Node):
    class Meta:
        name = 'customNode'

    @staticmethod
    def to_global_id(type, id):
        return id

class User(SQLAlchemyObjectType):
    """Users"""
    class Meta:
        model = UserModel
        interfaces = (CustomNode, )


class Post(SQLAlchemyObjectType):
    """Posts"""
    class Meta:
        model = PostModel
        interfaces = (CustomNode, )


class Vote(SQLAlchemyObjectType):
    """Posts"""
    class Meta:
        model = VoteModel
        interfaces = (CustomNode, )


class Query(graphene.ObjectType):
    """Query endpoint for GraphQL API"""
    node = CustomNode.Field()
    all_users = SQLAlchemyConnectionField(User.connection)
    all_posts = SQLAlchemyConnectionField(Post.connection)

    users_by_username = graphene.List(User, username=graphene.String())
    posts_by_filter = graphene.List(Post, filter_text=graphene.String())
    user = CustomNode.Field(User)
    post = CustomNode.Field(Post)

    @staticmethod
    def resolve_users_by_username(parent, info, **args):
        username = args.get('username')
        return User.get_query(info).filter(UserModel.username == username).all()

    @staticmethod
    def resolve_posts_by_filter(parent, info, **args):
        filter_text = args.get('filter_text')
        return Post.get_query(info).filter(PostModel.body.ilike(filter_text)).all()


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
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(User)
    auth_token = graphene.String()

    def mutate(self, info, **kwargs):
        user = UserModel.query.filter_by(email=kwargs.get('email')).first()
        if user is None or not user.verify_password(kwargs.get('password')):
            raise GraphQLError("Invalid Credentials")
        return Login(user=user, auth_token=user.encode_auth_token(user.id).decode())


class CreatePost(graphene.Mutation):
    class Arguments:
        body = graphene.String(required=True)

    post = graphene.Field(Post)

    @require_auth
    def mutate(self, info, **kwargs):
        author = kwargs.get('user')
        if not author:
            raise GraphQLError("Please log in to create this post")
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


class CreateVote(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)

    vote = graphene.Field(Vote)

    @require_auth
    def mutate(self, info, **kwargs):
        author = kwargs.get('user')
        if not author:
            raise GraphQLError("Please log in to vote")

        vote = VoteModel(post_id=kwargs.get('post_id'), author=author)
        db.session.add(vote)
        db.session.commit()
        return CreateVote(vote=vote)


class Mutation(graphene.ObjectType):
    """Mutation endpoint for GraphQL API"""
    signup = SignUp.Field()
    login = Login.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_vote = CreateVote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
