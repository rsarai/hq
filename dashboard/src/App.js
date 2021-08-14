import React from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';

import { Memex } from './pages/Memex';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Memex />
    </QueryClientProvider>
  );
}

export default App;
