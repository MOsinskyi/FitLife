import { createRouter, createWebHistory } from 'vue-router';
import { useAuth } from '../composables/useAuth';

import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ScheduleView from '../views/ScheduleView.vue';
import MembershipsView from '../views/MembershipsView.vue';
import CustomerDashboard from '../views/CustomerDashboard.vue';
import CoachDashboard from '../views/CoachDashboard.vue';
import ManagerDashboard from '../views/ManagerDashboard.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresGuest: true },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresGuest: true },
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: ScheduleView,
  },
  {
    path: '/memberships',
    name: 'memberships',
    component: MembershipsView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: CustomerDashboard,
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const { user } = useAuth();

      if (!user.value) {
        // Try to load user first
        const { loadUser } = useAuth();
        loadUser().then(() => {
          redirectToDashboard(next, user.value);
        });
      } else {
        redirectToDashboard(next, user.value);
      }
    },
  },
  {
    path: '/dashboard/customer',
    name: 'customer-dashboard',
    component: CustomerDashboard,
    meta: { requiresAuth: true, role: 'customer' },
  },
  {
    path: '/dashboard/coach',
    name: 'coach-dashboard',
    component: CoachDashboard,
    meta: { requiresAuth: true, role: 'coach' },
  },
  {
    path: '/dashboard/manager',
    name: 'manager-dashboard',
    component: ManagerDashboard,
    meta: { requiresAuth: true, role: 'manager' },
  },
];

function redirectToDashboard(next, user) {
  if (user?.role === 'customer') {
    next('/dashboard/customer');
  } else if (user?.role === 'coach') {
    next('/dashboard/coach');
  } else if (user?.role === 'manager') {
    next('/dashboard/manager');
  } else {
    next('/');
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const { isAuthenticated, loadUser, user } = useAuth();

  // Load user if authenticated but user data not loaded
  if (isAuthenticated.value && !user.value) {
    await loadUser();
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login');
    return;
  }

  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && isAuthenticated.value) {
    next('/dashboard');
    return;
  }

  // Check role-based access
  if (to.meta.role && user.value?.role !== to.meta.role) {
    next('/');
    return;
  }

  next();
});

export default router;
