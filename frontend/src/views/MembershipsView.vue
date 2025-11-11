<template>
  <div class="memberships-view">
    <div class="container">
      <h1>Membership Plans</h1>
      <p class="subtitle">Choose the perfect plan for your fitness journey</p>

      <div class="membership-types">
        <div class="membership-card basic">
          <div class="card-header">
            <h2>Basic</h2>
            <div class="price">$29<span>/month</span></div>
          </div>
          <ul class="features">
            <li>Access to gym facilities</li>
            <li>Standard equipment</li>
            <li>Locker room access</li>
            <li>2 group classes per month</li>
          </ul>
          <button
            v-if="isAuthenticated && hasRole('customer')"
            @click="selectMembership('basic', 29)"
            class="btn-select"
          >
            Select Plan
          </button>
          <router-link v-else to="/login" class="btn-select">Login to Select</router-link>
        </div>

        <div class="membership-card premium featured">
          <div class="badge">Most Popular</div>
          <div class="card-header">
            <h2>Premium</h2>
            <div class="price">$59<span>/month</span></div>
          </div>
          <ul class="features">
            <li>Everything in Basic</li>
            <li>Unlimited group classes</li>
            <li>Personal trainer consultation</li>
            <li>Nutrition planning</li>
            <li>Priority booking</li>
          </ul>
          <button
            v-if="isAuthenticated && hasRole('customer')"
            @click="selectMembership('premium', 59)"
            class="btn-select"
          >
            Select Plan
          </button>
          <router-link v-else to="/login" class="btn-select">Login to Select</router-link>
        </div>

        <div class="membership-card vip">
          <div class="card-header">
            <h2>VIP</h2>
            <div class="price">$99<span>/month</span></div>
          </div>
          <ul class="features">
            <li>Everything in Premium</li>
            <li>Unlimited personal training</li>
            <li>Spa and massage access</li>
            <li>Private locker</li>
            <li>Guest passes (5/month)</li>
            <li>24/7 gym access</li>
          </ul>
          <button
            v-if="isAuthenticated && hasRole('customer')"
            @click="selectMembership('vip', 99)"
            class="btn-select"
          >
            Select Plan
          </button>
          <router-link v-else to="/login" class="btn-select">Login to Select</router-link>
        </div>
      </div>

      <div v-if="myMemberships.length > 0" class="my-memberships">
        <h2>My Active Memberships</h2>
        <div class="memberships-list">
          <div
            v-for="membership in myMemberships"
            :key="membership.membership_id"
            class="membership-item"
          >
            <div class="membership-info">
              <h3>{{ membership.membership_type }} Membership</h3>
              <p>Started: {{ formatDate(membership.start_date) }}</p>
              <p>Expires: {{ formatDate(membership.end_date) }}</p>
              <p>Status: <span class="status">{{ membership.status }}</span></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { membershipsAPI } from '../services/api';
import { useAuth } from '../composables/useAuth';

const { isAuthenticated, user, hasRole } = useAuth();

const myMemberships = ref([]);

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const selectMembership = async (type, price) => {
  if (!user.value?.customer_id) {
    alert('Customer information not found');
    return;
  }

  const startDate = new Date();
  const endDate = new Date();
  endDate.setMonth(endDate.getMonth() + 1);

  try {
    await membershipsAPI.create({
      customer_id: user.value.customer_id,
      membership_type: type,
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0],
      price: price,
      status: 'active',
    });

    alert(`Successfully subscribed to ${type} membership!`);
    await loadMyMemberships();
  } catch (error) {
    console.error('Membership error:', error);
    alert(error.response?.data?.detail || 'Failed to create membership');
  }
};

const loadMyMemberships = async () => {
  if (user.value?.customer_id) {
    try {
      const data = await membershipsAPI.getByCustomer(user.value.customer_id);
      myMemberships.value = data;
    } catch (error) {
      console.error('Error loading memberships:', error);
    }
  }
};

onMounted(() => {
  if (isAuthenticated.value && hasRole('customer')) {
    loadMyMemberships();
  }
});
</script>

<style scoped>
.memberships-view {
  min-height: 100vh;
  padding: 40px 20px;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.subtitle {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

.membership-types {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.membership-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.3s;
}

.membership-card:hover {
  transform: translateY(-10px);
}

.membership-card.featured {
  border: 3px solid #667eea;
  transform: scale(1.05);
}

.badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.card-header {
  text-align: center;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 1.5rem;
}

.card-header h2 {
  color: #333;
  font-size: 2rem;
  margin-bottom: 1rem;
}

.price {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
}

.price span {
  font-size: 1.2rem;
  color: #666;
  font-weight: normal;
}

.features {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
}

.features li {
  padding: 0.8rem 0;
  color: #555;
  border-bottom: 1px solid #f0f0f0;
}

.features li:before {
  content: '✓ ';
  color: #667eea;
  font-weight: bold;
  margin-right: 0.5rem;
}

.btn-select {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s;
  text-decoration: none;
  display: block;
  text-align: center;
}

.btn-select:hover {
  transform: scale(1.02);
}

.my-memberships {
  margin-top: 4rem;
}

.my-memberships h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.memberships-list {
  display: grid;
  gap: 1.5rem;
}

.membership-item {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #667eea;
}

.membership-info h3 {
  color: #333;
  margin-bottom: 1rem;
  text-transform: capitalize;
}

.membership-info p {
  color: #666;
  margin-bottom: 0.5rem;
}

.status {
  color: #667eea;
  font-weight: 600;
  text-transform: capitalize;
}
</style>
