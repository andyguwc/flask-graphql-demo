import React from 'react';
import '../styles/App.css';
import { Switch, Route } from 'react-router-dom';
import PostList from './PostList';
import CreatePost from './CreatePost';
import Header from './Header';

function App() {
  return (
    <div className="center w85">
      <Header />
      <div className="ph3 pv1 background-gray">
        <Switch>
          <Route exact path="/" component={PostList} />
          <Route exact path="/create" component={CreatePost} />
        </Switch>
      </div>
    </div>
  );
}

export default App;
