import React from 'react';
import { useInfiniteQuery } from 'react-query';
import axios from 'utils/axios';

export function useNodesInfinity(queryParams) {
  return useInfiniteQuery(['infinite-nodes', queryParams], useLogs, {
    refetchOnWindowFocus: false,
    getNextPageParam: (lastPage, pages) =>
      lastPage.next_page_number ? lastPage.next_page_number : false,
  });
}

export const useLogs = async ({ queryKey, pageParam = 1 }) => {
  const queryParams = queryKey[1];
  const res = await axios.get(
    'http://127.0.0.1:5000/api/nodes/?page=' + pageParam + '&' + queryParams
  );
  return res.data;
};
