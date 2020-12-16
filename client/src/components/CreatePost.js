import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { useHistory } from 'react-router';

const CREATE_POST_MUTATION = gql`
  mutation CreatePostMutation($body: String!) {
    createPost(body: $body) {
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
  const history = useHistory();

  const [formState, setFormState] = useState({
    body: '',
  });

  const [createPost] = useMutation(CREATE_POST_MUTATION, {
    variables: {
      body: formState.body,
    },
    onCompleted: () => history.push('/'),
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
