import React, { useState } from 'react';
import { useToggle } from 'react-use';
import styled from 'styled-components';

import { getDateFromEvent } from 'utils/dates';
import { useNodesInfinity } from 'hooks/useMemex';
// import { useIntersectionObserver } from 'hooks/useIntersectionObserver';

const Container = styled.div`
  font-family: 'IBM Plex Sans', sans-serif;
  max-width: 900px;
  margin: auto;
`;

const SearchField = styled.div`
  width: 100%;
`;

const LayoutList = styled.div`
  margin: 0 10px;
  display: flex;
  flex-direction: column;
`;

const SimpleEvent = styled.div`
  padding: 10px 20px;
  background-color: white;
  color: #3a2f45;
  border: 1px solid #white;
  border-radius: 10px;
  box-shadow: 2px -1px 8px #c5c5cc;

  .detail {
    color: #7B7C7C;
    font-size: 13px;
  }
`;

const Dot = styled.div`
  height: 5px;
  width: 5px;
  background-color: #747474;
  border-radius: 50%;
  display: inline-block;
  margin-bottom: 2px;
`;

export const Memex = () => {
  const [queryParams, setQueryParams] = useState('');
  const [shortMode, setShortMode] = useToggle(true);
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useNodesInfinity(queryParams);

  // const loadMoreButtonRef = React.useRef();
  // useIntersectionObserver({
  //   target: loadMoreButtonRef,
  //   onIntersect: fetchNextPage,
  //   enabled: hasNextPage,
  // });

  return (
    <Container>
      <h4>
        <b>Memex</b>, a single place for my data
      </h4>
      <SearchField>
        <input
          id='queryParams'
          name='queryParams'
          type='text'
          style={{ width: '100%', height: '25px' }}
          autoComplete='off'
          placeholder='Full text search...'
          defaultValue={queryParams}
        />
      </SearchField>
      <br></br>
      {data ? (
        <LayoutList>
          <h6>
            Found {data.pages[0].count} results{' '}
            {queryParams ? `for term: ${queryParams}` : null}
          </h6>
          {data.pages.map((page, i) => (
            <>
              {page.results.map((log, index) => (
                <>
                  <SimpleEvent>
                    <h5>{log.title ? log.title : log.provider}</h5>
                    <small>
                      {log.provider} <Dot /> {log.activity} <Dot />{' '}
                      {log.activity_entities} <Dot /> {getDateFromEvent(log)}
                    </small>
                    <p>
                      {Object.keys(log).map((key) => {
                        if (typeof log[key] != 'object') {
                          return (
                            <span>
                              <span className='detail'>{key}</span> {log[key]}
                              {'   |   '}
                            </span>
                          );
                        }
                        return '';
                      })}
                    </p>
                  </SimpleEvent>
                  <br></br>
                </>
              ))}
            </>
          ))}
        </LayoutList>
      ) : null}
    </Container>
  );
};
