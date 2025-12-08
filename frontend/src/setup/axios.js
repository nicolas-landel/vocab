import axios from 'axios'
import {
  transformObjectToSnakeCase,
  transformObjectToCamelCase,
} from "@/utils/caseTransform.js";


const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
})

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)


apiClient.interceptors.request.use(
  (config) => {
    if (config.data) {
      config.data = transformObjectToSnakeCase(config.data);
    }
    if (config.params) {
      config.params = transformObjectToSnakeCase(config.params);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Transform response data from snake_case to camelCase
apiClient.interceptors.response.use(
  (response) => {
    if (response.data) {
      response.data = transformObjectToCamelCase(response.data);
    }
    return response;
  },
  (error) => {
    if (error.response?.data) {
      error.response.data = transformObjectToCamelCase(error.response.data);
    }
    return Promise.reject(error);
  },
);


export default apiClient
