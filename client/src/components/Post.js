import React from 'react';

const Post = (props) => {
  const { post } = props;
  return (
    <>
      <div>{post.body}</div>
    </>
  );
};

export default Post;
