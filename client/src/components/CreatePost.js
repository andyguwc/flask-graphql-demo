import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';

const CREATE_POST_MUTATION = gql`
  mutation CreatePostMutation($body: String!, $authorId: Int!) {
    createPost(body: $body, authorId: $authorId) {
      post {
        id
        authorId
        body
        author {
          username
          email
        }
      }
    }
  }
`;

const CreatePost = () => {
  const [formState, setFormState] = useState({
    body: '',
  });

  const [createPost] = useMutation(CREATE_POST_MUTATION, {
    variables: {
      body: formState.body,
      authorId: 5,
    },
  });

  return (
    <>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          createPost();
        }}
      >
        <div className="flex flex-column mt3">
          <input
            className="mb2"
            value={formState.body}
            onChange={(e) =>
              setFormState({
                ...formState,
                body: e.target.value,
              })
            }
            type="text"
            placeholder="Post body"
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </>
  );
};

export default CreatePost;
