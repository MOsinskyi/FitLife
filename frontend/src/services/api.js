import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Users/Managers API
export const usersAPI = {
  create: async (userData) => {
    const response = await api.post('/users/', userData);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/users/');
    return response.data;
  },
};

// Customers API
export const customersAPI = {
  create: async (customerData) => {
    const response = await api.post('/customers/', customerData);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/customers/');
    return response.data;
  },

  getById: async (customerId) => {
    const response = await api.get(`/customers/${customerId}`);
    return response.data;
  },

  update: async (customerId, customerData) => {
    const response = await api.put(`/customers/${customerId}`, customerData);
    return response.data;
  },
};

// Coaches API
export const coachesAPI = {
  create: async (coachData) => {
    const response = await api.post('/coaches/', coachData);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/coaches/');
    return response.data;
  },

  getById: async (coachId) => {
    const response = await api.get(`/coaches/${coachId}`);
    return response.data;
  },
};

// Schedules API
export const schedulesAPI = {
  create: async (scheduleData) => {
    const response = await api.post('/schedules/', scheduleData);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/schedules/');
    return response.data;
  },

  getById: async (scheduleId) => {
    const response = await api.get(`/schedules/${scheduleId}`);
    return response.data;
  },

  getAvailable: async () => {
    const response = await api.get('/schedules/available');
    return response.data;
  },
};

// Bookings API
export const bookingsAPI = {
  create: async (bookingData) => {
    const response = await api.post('/bookings/', bookingData);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/bookings/');
    return response.data;
  },

  getByCustomer: async (customerId) => {
    const response = await api.get(`/bookings/customer/${customerId}`);
    return response.data;
  },

  getBySchedule: async (scheduleId) => {
    const response = await api.get(`/bookings/schedule/${scheduleId}`);
    return response.data;
  },

  cancel: async (bookingId) => {
    const response = await api.delete(`/bookings/${bookingId}`);
    return response.data;
  },
};

// Memberships API
export const membershipsAPI = {
  create: async (membershipData) => {
    const response = await api.post('/memberships/', membershipData);
    return response.data;
  },

  getAll: async () => {
    const response = await api.get('/memberships/');
    return response.data;
  },

  getByCustomer: async (customerId) => {
    const response = await api.get(`/memberships/customer/${customerId}`);
    return response.data;
  },
};

export default api;
