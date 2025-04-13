"use client";

import {
  QueryClient,
  QueryClientProvider,
  createApiClient,
} from "@typethon/api-client";
import { useState } from "react";

export const api = createApiClient({
  baseUrl: "http://localhost:8000",
});

export const ApiProvider = ({ children }: { children: React.ReactNode }) => {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};
