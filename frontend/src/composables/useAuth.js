import { ref, computed } from 'vue';
import { authAPI } from '../services/api';

const token = ref(localStorage.getItem('token') || null);
const user = ref(null);

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);
      token.value = response.access_token;
      localStorage.setItem('token', response.access_token);

      // Get user info
      const userData = await authAPI.getCurrentUser();
      user.value = userData;

      return { success: true };
    } catch (error) {
      console.error('Login error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Login failed'
      };
    }
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
  };

  const loadUser = async () => {
    if (token.value && !user.value) {
      try {
        const userData = await authAPI.getCurrentUser();
        user.value = userData;
      } catch (error) {
        console.error('Failed to load user:', error);
        logout();
      }
    }
  };

  const hasRole = (role) => {
    return user.value?.role === role;
  };

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    loadUser,
    hasRole,
  };
}
