import React from 'react';
import { useMutation, gql } from '@apollo/client';
import { AUTH_TOKEN, POSTS_PER_PAGE } from '../constants';
import { timeDifferenceForDate } from '../utils';
import { GET_POSTS_QUERY } from './PostList';

const VOTE_MUTATION = gql`
  mutation VoteMutation($postId: Int!) {
    createVote(postId: $postId) {
      vote {
        id
        post {
          id
          author {
            id
          }
        }
        author {
          id
        }
      }
    }
  }
`;

const Post = (props) => {
  const { post } = props;
  const authToken = localStorage.getItem(AUTH_TOKEN);

  const [vote] = useMutation(VOTE_MUTATION, {
    variables: {
      postId: post.id,
    },
    update: (cache, { data: { vote } }) => {
      const { allPosts } = cache.readQuery({
        query: GET_POSTS_QUERY,
      });

      console.log(allPosts);

      const updatedPosts = allPosts.edges.map(({ node }) => {
        if (node.id === post.id) {
          const newPost = {
            ...node,
            votes: { edges: [...node.votes.edges, vote] },
          };
          return newPost;
        }
        return node;
      });

      cache.writeQuery({
        query: GET_POSTS_QUERY,
        data: {
          allPosts: {
            edges: updatedPosts,
          },
        },
      });
    },
  });

  return (
    <div className="flex mt2 items-start">
      <div className="flex items-center">
        <span className="gray">{props.index + 1}.</span>
        {authToken && (
          <div
            className="ml1 gray f11"
            style={{ cursor: 'pointer' }}
            onClick={vote}
          >
            ▲
          </div>
        )}
      </div>
      <div className="ml1">
        <div>
          {post.body}
          {authToken && (
            <div className="f6 lh-copy gray">
              {post.votes.edges.length} votes | by{' '}
              {post.author ? post.author.username : 'Unknown'}{' '}
              {timeDifferenceForDate(post.timestamp)}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Post;
