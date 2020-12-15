import React from 'react';
import Post from './Post';
import { useQuery, gql } from '@apollo/client';

const GET_POSTS_QUERY = gql`
  query {
    allPosts {
      edges {
        node {
          id
          body
        }
      }
    }
  }
`;

const PostList = () => {
  const { data } = useQuery(GET_POSTS_QUERY);

  return (
    <>
      {data && (
        <>
          {data.allPosts.edges.map(({ node }) => (
            <Post key={node.id} post={node} />
          ))}
        </>
      )}
    </>
  );
};

export default PostList;
