import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL !== undefined && import.meta.env.VITE_API_URL !== ''
  ? import.meta.env.VITE_API_URL
  : (import.meta.env.DEV ? 'http://127.0.0.1:8000' : '');

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 120000, // 2 min — occlusion heatmap can be slow
});

export const checkHealth = () => apiClient.get('/api/health');

export const predictImage = (file, onUploadProgress) =>
  apiClient.post('/api/v1/predict', (() => {
    const fd = new FormData();
    fd.append('image', file);
    return fd;
  })(), {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  });
