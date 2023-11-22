import React, { useState } from 'react';
import { useQuery } from 'react-query';
import styled from 'styled-components';

import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';

import axios from 'utils/axios';
import { getDateFromEvent } from 'utils/dates';
import { useNodesInfinity } from 'hooks/useMemex';

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
    color: #7b7c7c;
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

export const getProviders = async () => {
  const res = await axios.get('http://127.0.0.1:5000/api/providers/');
  return res.data;
};

export const Memex = () => {
  const [queryParams, setQueryParams] = useState('');
  const [search, setSearch] = useState('');
  const [provider, setProvider] = useState('');
  const { data: providersQuery, isLoading } = useQuery(
    'providers',
    getProviders
  );

  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useNodesInfinity(queryParams);

  const handleProviderChange = (e) => {
    setProvider(e.target.value);
  };

  const handleInputChange = (e) => {
    setSearch(e.target.value);
  };

  const handleOnClick = (e) => {
    if (provider && search) {
      setQueryParams(`provider=${provider}&qs=${search}`);
    } else if (provider) {
      setQueryParams(`provider=${provider}`);
    } else if (search) {
      setQueryParams(`qs=${search}`);
    }
  };

  return (
    <Container>
      <h4>
        <b>Memex</b>, a single place for my data
      </h4>
      <div style={{ display: 'flex', backgroundColor: 'white' }}>
        {isLoading ? (
          <div></div>
        ) : (
          <div>
            <Box sx={{ minWidth: 120 }}>
              <FormControl fullWidth>
                <InputLabel id='provider-select-label'>Providers</InputLabel>
                <Select
                  labelId='provider-simple-select-label'
                  id='provider-simple-select'
                  value={provider}
                  label='Provider'
                  onChange={handleProviderChange}
                >
                  {providersQuery.results
                    ? providersQuery.results.map((item) => {
                        return (
                          <MenuItem value={item.value}>{item.label}</MenuItem>
                        );
                      })
                    : ''}
                </Select>
              </FormControl>
            </Box>
          </div>
        )}
        <TextField
          fullWidth
          id='outlined-basic'
          label='Full text search...'
          variant='outlined'
          onChange={handleInputChange}
          value={search}
        />
        <Button onClick={handleOnClick}>Go</Button>
      </div>
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
      {hasNextPage ? (
        <Button variant='contained' onClick={fetchNextPage}>
          Next
        </Button>
      ) : (
        ''
      )}
    </Container>
  );
};
