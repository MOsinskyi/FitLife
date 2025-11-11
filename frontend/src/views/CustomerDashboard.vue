<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1>Welcome, {{ user?.full_name }}</h1>
        <p class="role-badge">Customer Dashboard</p>
      </div>

      <div class="dashboard-grid">
        <div class="card stats-card">
          <h2>Quick Stats</h2>
          <div class="stats">
            <div class="stat-item">
              <div class="stat-value">{{ myBookings.length }}</div>
              <div class="stat-label">Active Bookings</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ myMemberships.length }}</div>
              <div class="stat-label">Memberships</div>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>My Bookings</h2>
          <div v-if="loadingBookings" class="loading">Loading...</div>
          <div v-else-if="myBookings.length === 0" class="no-data">
            No bookings yet. <router-link to="/schedule">Book a session</router-link>
          </div>
          <div v-else class="bookings-list">
            <div
              v-for="booking in myBookings"
              :key="booking.booking_id"
              class="booking-item"
            >
              <div class="booking-info">
                <h3>{{ getScheduleInfo(booking.schedule_id)?.training_type }}</h3>
                <p>{{ formatDate(getScheduleInfo(booking.schedule_id)?.date) }}</p>
                <p>
                  {{ getScheduleInfo(booking.schedule_id)?.start_time }} -
                  {{ getScheduleInfo(booking.schedule_id)?.end_time }}
                </p>
                <p>Status: <span class="status">{{ booking.status }}</span></p>
              </div>
              <button
                v-if="booking.status === 'confirmed'"
                @click="cancelBooking(booking.booking_id)"
                class="btn-cancel"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>My Memberships</h2>
          <div v-if="loadingMemberships" class="loading">Loading...</div>
          <div v-else-if="myMemberships.length === 0" class="no-data">
            No active memberships. <router-link to="/memberships">View plans</router-link>
          </div>
          <div v-else class="memberships-list">
            <div
              v-for="membership in myMemberships"
              :key="membership.membership_id"
              class="membership-item"
            >
              <h3>{{ membership.membership_type }} Plan</h3>
              <p>Started: {{ formatDate(membership.start_date) }}</p>
              <p>Expires: {{ formatDate(membership.end_date) }}</p>
              <p>
                Status:
                <span class="status" :class="membership.status">{{
                  membership.status
                }}</span>
              </p>
              <p class="price">${{ membership.price }}/month</p>
            </div>
          </div>
        </div>

        <div class="card actions-card">
          <h2>Quick Actions</h2>
          <div class="actions">
            <router-link to="/schedule" class="action-btn">
              <span class="icon">📅</span>
              <span>Book Training</span>
            </router-link>
            <router-link to="/memberships" class="action-btn">
              <span class="icon">💳</span>
              <span>View Plans</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { bookingsAPI, membershipsAPI, schedulesAPI } from '../services/api';
import { useAuth } from '../composables/useAuth';

const { user } = useAuth();

const myBookings = ref([]);
const myMemberships = ref([]);
const schedules = ref([]);
const loadingBookings = ref(true);
const loadingMemberships = ref(true);

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const getScheduleInfo = (scheduleId) => {
  return schedules.value.find((s) => s.schedule_id === scheduleId);
};

const cancelBooking = async (bookingId) => {
  if (!confirm('Are you sure you want to cancel this booking?')) return;

  try {
    await bookingsAPI.cancel(bookingId);
    alert('Booking cancelled successfully');
    await loadBookings();
  } catch (error) {
    console.error('Cancel error:', error);
    alert('Failed to cancel booking');
  }
};

const loadBookings = async () => {
  if (!user.value?.customer_id) return;

  try {
    loadingBookings.value = true;
    const [bookingsData, schedulesData] = await Promise.all([
      bookingsAPI.getByCustomer(user.value.customer_id),
      schedulesAPI.getAll(),
    ]);

    myBookings.value = bookingsData;
    schedules.value = schedulesData;
  } catch (error) {
    console.error('Error loading bookings:', error);
  } finally {
    loadingBookings.value = false;
  }
};

const loadMemberships = async () => {
  if (!user.value?.customer_id) return;

  try {
    loadingMemberships.value = true;
    const data = await membershipsAPI.getByCustomer(user.value.customer_id);
    myMemberships.value = data;
  } catch (error) {
    console.error('Error loading memberships:', error);
  } finally {
    loadingMemberships.value = false;
  }
};

onMounted(() => {
  loadBookings();
  loadMemberships();
});
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 40px 20px;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
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
}

.card h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  color: white;
}

.stat-value {
  font-size: 3rem;
  font-weight: bold;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
}

.loading,
.no-data {
  text-align: center;
  color: #666;
  padding: 2rem 0;
}

.no-data a {
  color: #667eea;
  font-weight: 600;
}

.bookings-list,
.memberships-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.booking-item,
.membership-item {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.booking-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.booking-info h3,
.membership-item h3 {
  color: #333;
  margin-bottom: 0.5rem;
  text-transform: capitalize;
}

.booking-info p,
.membership-item p {
  color: #666;
  margin-bottom: 0.3rem;
  font-size: 0.95rem;
}

.status {
  font-weight: 600;
  text-transform: capitalize;
}

.status.confirmed,
.status.active {
  color: #28a745;
}

.status.cancelled,
.status.expired {
  color: #dc3545;
}

.price {
  color: #667eea;
  font-weight: bold;
  font-size: 1.1rem;
}

.btn-cancel {
  padding: 0.5rem 1rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.btn-cancel:hover {
  background: #c82333;
}

.actions {
  display: grid;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: transform 0.2s;
}

.action-btn:hover {
  transform: translateX(5px);
}

.action-btn .icon {
  font-size: 2rem;
}
</style>
