<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1>Welcome, {{ user?.full_name }}</h1>
        <p class="role-badge">Manager Dashboard</p>
      </div>

      <div class="dashboard-grid">
        <div class="card stats-card full-width">
          <h2>System Overview</h2>
          <div class="stats">
            <div class="stat-item">
              <div class="stat-value">{{ customers.length }}</div>
              <div class="stat-label">Customers</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ coaches.length }}</div>
              <div class="stat-label">Coaches</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ schedules.length }}</div>
              <div class="stat-label">Schedules</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ bookings.length }}</div>
              <div class="stat-label">Bookings</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ memberships.length }}</div>
              <div class="stat-label">Memberships</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ managers.length }}</div>
              <div class="stat-label">Managers</div>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>Customers</h2>
          <div v-if="loadingCustomers" class="loading">Loading...</div>
          <div v-else-if="customers.length === 0" class="no-data">No customers yet</div>
          <div v-else class="list">
            <div v-for="customer in customers" :key="customer.customer_id" class="list-item">
              <div>
                <h4>{{ customer.full_name }}</h4>
                <p>{{ customer.email }}</p>
                <p>{{ customer.phone }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>Coaches</h2>
          <div v-if="loadingCoaches" class="loading">Loading...</div>
          <div v-else-if="coaches.length === 0" class="no-data">No coaches yet</div>
          <div v-else class="list">
            <div v-for="coach in coaches" :key="coach.coach_id" class="list-item">
              <div>
                <h4>{{ coach.full_name }}</h4>
                <p>{{ coach.email }}</p>
                <p>Specialization: {{ coach.specialization }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card full-width">
          <h2>All Training Sessions</h2>
          <div v-if="loadingSchedules" class="loading">Loading...</div>
          <div v-else-if="schedules.length === 0" class="no-data">No schedules yet</div>
          <div v-else class="schedules-grid">
            <div
              v-for="schedule in schedules"
              :key="schedule.schedule_id"
              class="schedule-card"
            >
              <h4>{{ schedule.training_type }}</h4>
              <p>Coach: {{ getCoachName(schedule.coach_id) }}</p>
              <p>{{ formatDate(schedule.date) }}</p>
              <p>{{ schedule.start_time }} - {{ schedule.end_time }}</p>
              <p>Capacity: {{ schedule.capacity }} spots</p>
              <p>Bookings: {{ getScheduleBookings(schedule.schedule_id) }}</p>
            </div>
          </div>
        </div>

        <div class="card full-width">
          <h2>Recent Bookings</h2>
          <div v-if="loadingBookings" class="loading">Loading...</div>
          <div v-else-if="bookings.length === 0" class="no-data">No bookings yet</div>
          <div v-else class="list">
            <div v-for="booking in bookings.slice(0, 10)" :key="booking.booking_id" class="list-item">
              <div>
                <h4>Booking #{{ booking.booking_id }}</h4>
                <p>Customer ID: {{ booking.customer_id }}</p>
                <p>Schedule ID: {{ booking.schedule_id }}</p>
                <p>Status: <span class="status">{{ booking.status }}</span></p>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>Create Manager Account</h2>
          <form @submit.prevent="createManager" class="form">
            <div class="form-group">
              <label>Full Name</label>
              <input v-model="newManager.full_name" type="text" required />
            </div>
            <div class="form-group">
              <label>Email</label>
              <input v-model="newManager.email" type="email" required />
            </div>
            <div class="form-group">
              <label>Password</label>
              <input v-model="newManager.password" type="password" required />
            </div>
            <button type="submit" class="btn-create" :disabled="creatingManager">
              {{ creatingManager ? 'Creating...' : 'Create Manager' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import {
  customersAPI,
  coachesAPI,
  schedulesAPI,
  bookingsAPI,
  membershipsAPI,
  usersAPI,
} from '../services/api';
import { useAuth } from '../composables/useAuth';

const { user } = useAuth();

const customers = ref([]);
const coaches = ref([]);
const schedules = ref([]);
const bookings = ref([]);
const memberships = ref([]);
const managers = ref([]);

const loadingCustomers = ref(true);
const loadingCoaches = ref(true);
const loadingSchedules = ref(true);
const loadingBookings = ref(true);
const loadingMemberships = ref(true);
const creatingManager = ref(false);

const newManager = ref({
  full_name: '',
  email: '',
  password: '',
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

const getCoachName = (coachId) => {
  const coach = coaches.value.find((c) => c.coach_id === coachId);
  return coach ? coach.full_name : 'Unknown';
};

const getScheduleBookings = (scheduleId) => {
  return bookings.value.filter((b) => b.schedule_id === scheduleId).length;
};

const createManager = async () => {
  creatingManager.value = true;

  try {
    await usersAPI.create({
      full_name: newManager.value.full_name,
      email: newManager.value.email,
      password: newManager.value.password,
    });

    alert('Manager account created successfully!');
    newManager.value = {
      full_name: '',
      email: '',
      password: '',
    };

    await loadManagers();
  } catch (error) {
    console.error('Create manager error:', error);
    alert(error.response?.data?.detail || 'Failed to create manager');
  } finally {
    creatingManager.value = false;
  }
};

const loadCustomers = async () => {
  try {
    loadingCustomers.value = true;
    customers.value = await customersAPI.getAll();
  } catch (error) {
    console.error('Error loading customers:', error);
  } finally {
    loadingCustomers.value = false;
  }
};

const loadCoaches = async () => {
  try {
    loadingCoaches.value = true;
    coaches.value = await coachesAPI.getAll();
  } catch (error) {
    console.error('Error loading coaches:', error);
  } finally {
    loadingCoaches.value = false;
  }
};

const loadSchedules = async () => {
  try {
    loadingSchedules.value = true;
    schedules.value = await schedulesAPI.getAll();
  } catch (error) {
    console.error('Error loading schedules:', error);
  } finally {
    loadingSchedules.value = false;
  }
};

const loadBookings = async () => {
  try {
    loadingBookings.value = true;
    bookings.value = await bookingsAPI.getAll();
  } catch (error) {
    console.error('Error loading bookings:', error);
  } finally {
    loadingBookings.value = false;
  }
};

const loadMemberships = async () => {
  try {
    loadingMemberships.value = true;
    memberships.value = await membershipsAPI.getAll();
  } catch (error) {
    console.error('Error loading memberships:', error);
  } finally {
    loadingMemberships.value = false;
  }
};

const loadManagers = async () => {
  try {
    managers.value = await usersAPI.getAll();
  } catch (error) {
    console.error('Error loading managers:', error);
  }
};

onMounted(async () => {
  await Promise.all([
    loadCustomers(),
    loadCoaches(),
    loadSchedules(),
    loadBookings(),
    loadMemberships(),
    loadManagers(),
  ]);
});
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 40px 20px;
  background: #f8f9fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.role-badge {
  color: #667eea;
  font-size: 1.1rem;
  font-weight: 600;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 600px;
  overflow-y: auto;
}

.card.full-width {
  grid-column: 1 / -1;
}

.card h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  position: sticky;
  top: 0;
  background: white;
  padding-bottom: 1rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.95rem;
  opacity: 0.9;
}

.loading,
.no-data {
  text-align: center;
  color: #666;
  padding: 2rem 0;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.list-item {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.list-item h4 {
  color: #333;
  margin-bottom: 0.3rem;
}

.list-item p {
  color: #666;
  margin-bottom: 0.2rem;
  font-size: 0.9rem;
}

.status {
  font-weight: 600;
  text-transform: capitalize;
  color: #28a745;
}

.schedules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.schedule-card {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.schedule-card h4 {
  color: #333;
  margin-bottom: 0.5rem;
}

.schedule-card p {
  color: #666;
  margin-bottom: 0.3rem;
  font-size: 0.85rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-create {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-create:hover:not(:disabled) {
  transform: scale(1.02);
}

.btn-create:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
