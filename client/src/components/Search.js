import React, { useState } from 'react';
import { useLazyQuery, gql } from '@apollo/client';
import Post from './Post';

const POST_SEARCH_QUERY = gql`
  query PostSearchQuery($filterText: String!) {
    postsByFilter(filterText: $filterText) {
      body
      id
      votes {
        edges {
          node {
            id
            author {
              id
            }
          }
        }
      }
    }
  }
`;

const Search = () => {
  const [searchFilter, setSearchFilter] = useState('');
  const [executeSearch, { data }] = useLazyQuery(POST_SEARCH_QUERY);
  return (
    <>
      <div>
        Search
        <input type="text" onChange={(e) => setSearchFilter(e.target.value)} />
        <button
          onClick={() =>
            executeSearch({
              variables: { filterText: `%${searchFilter}%` },
            })
          }
        >
          OK
        </button>
      </div>
      {data &&
        data.postsByFilter.map((post, index) => (
          <Post key={post.id} post={post} index={index} />
        ))}
    </>
  );
};

export default Search;
