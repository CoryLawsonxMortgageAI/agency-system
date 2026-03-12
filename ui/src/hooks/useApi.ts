import { useState, useEffect, useCallback } from 'react';

const API_BASE_URL = '/api/v1';

// Get auth token from localStorage
const getToken = () => localStorage.getItem('agency_token');

// Fetch with auth
async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = getToken();
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...options.headers as Record<string, string>,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers,
  });
  
  if (response.status === 401) {
    // Token expired or invalid
    localStorage.removeItem('agency_token');
    window.location.reload();
    throw new Error('Unauthorized');
  }
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

export function useApi<T>(endpoint: string, interval?: number) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const result = await fetchWithAuth(`${API_BASE_URL}${endpoint}`);
      setData(result);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    fetchData();
    
    if (interval) {
      const timer = setInterval(fetchData, interval);
      return () => clearInterval(timer);
    }
  }, [fetchData, interval]);

  return { data, loading, error, refetch: fetchData };
}

export async function postApi<T>(endpoint: string, data?: any): Promise<T> {
  return fetchWithAuth(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  });
}

export default { useApi, postApi, fetchWithAuth };
