import React from 'react';
import '../styles/App.css';

import PostList from './PostList';
import CreatePost from './CreatePost';

function App() {
  return (
    <>
      <PostList />
      <CreatePost />
    </>
  );
}

export default App;
