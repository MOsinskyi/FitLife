<template>
  <header class="header">
    <div class="header-top">
      <div class="star-icon">⭐</div>
    </div>
    <div class="container">
      <nav class="nav">
        <a href="#about" class="nav-link">About</a>
        <a href="#gallery" class="nav-link">Gallery</a>
        <a href="#memberships" class="nav-link">Memberships</a>
        <a href="#price" class="nav-link">Price</a>
        <a href="#gallery" class="nav-link">Gallery</a>
        <a href="#zones-services" class="nav-link">Zones</a>
        <a href="#booking" class="nav-link">Contact</a>

        <template v-if="isAuthenticated">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <button @click="handleLogout" class="btn-logout">Logout</button>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';

const router = useRouter();
const { isAuthenticated, logout } = useAuth();

const handleLogout = () => {
  logout();
  router.push('/');
};
</script>

<style scoped>
.header {
  background: #8b9198;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-top {
  background: #6d757d;
  padding: 0.5rem;
  text-align: left;
  padding-left: 2rem;
}

.star-icon {
  font-size: 1.5rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav {
  display: flex;
  gap: 2rem;
  align-items: center;
  justify-content: center;
  padding: 1rem 0;
  flex-wrap: wrap;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9rem;
  text-transform: uppercase;
  transition: opacity 0.3s;
  letter-spacing: 0.5px;
}

.nav-link:hover {
  opacity: 0.7;
}

.btn-logout {
  background: #5a6268;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 0.9rem;
  text-transform: uppercase;
}

.btn-logout:hover {
  background: #4a5258;
}

@media (max-width: 768px) {
  .nav {
    gap: 1rem;
    font-size: 0.8rem;
  }

  .nav-link {
    font-size: 0.8rem;
  }
}
</style>
