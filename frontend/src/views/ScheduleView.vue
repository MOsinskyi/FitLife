<template>
  <div class="schedule-view">
    <div class="container">
      <h1>Training Schedule</h1>
      <p class="subtitle">Browse available training sessions and book your spot</p>

      <div v-if="loading" class="loading">Loading schedules...</div>

      <div v-if="error" class="error-message">{{ error }}</div>

      <div class="filters">
        <button
          :class="{ active: filter === 'all' }"
          @click="filter = 'all'"
          class="filter-btn"
        >
          All Sessions
        </button>
        <button
          :class="{ active: filter === 'available' }"
          @click="filter = 'available'"
          class="filter-btn"
        >
          Available Only
        </button>
      </div>

      <div v-if="filteredSchedules.length === 0 && !loading" class="no-data">
        No training sessions available at the moment.
      </div>

      <div class="schedules-grid">
        <div
          v-for="schedule in filteredSchedules"
          :key="schedule.schedule_id"
          class="schedule-card"
        >
          <div class="schedule-header">
            <h3>{{ schedule.training_type }}</h3>
            <span
              class="status-badge"
              :class="{ available: schedule.capacity > 0, full: schedule.capacity === 0 }"
            >
              {{ schedule.capacity > 0 ? 'Available' : 'Full' }}
            </span>
          </div>

          <div class="schedule-details">
            <div class="detail-item">
              <strong>Date:</strong> {{ formatDate(schedule.date) }}
            </div>
            <div class="detail-item">
              <strong>Time:</strong> {{ schedule.start_time }} - {{ schedule.end_time }}
            </div>
            <div class="detail-item">
              <strong>Coach:</strong> {{ getCoachName(schedule.coach_id) }}
            </div>
            <div class="detail-item">
              <strong>Capacity:</strong> {{ schedule.capacity }} spots left
            </div>
          </div>

          <button
            v-if="isAuthenticated && hasRole('customer') && schedule.capacity > 0"
            @click="bookSession(schedule.schedule_id)"
            class="btn-book"
            :disabled="bookingInProgress === schedule.schedule_id"
          >
            {{ bookingInProgress === schedule.schedule_id ? 'Booking...' : 'Book Now' }}
          </button>

          <div v-if="!isAuthenticated" class="login-prompt">
            <router-link to="/login">Login to book</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { schedulesAPI, coachesAPI, bookingsAPI } from '../services/api';
import { useAuth } from '../composables/useAuth';

const { isAuthenticated, user, hasRole } = useAuth();

const schedules = ref([]);
const coaches = ref([]);
const loading = ref(true);
const error = ref('');
const filter = ref('all');
const bookingInProgress = ref(null);

const filteredSchedules = computed(() => {
  if (filter.value === 'available') {
    return schedules.value.filter((s) => s.capacity > 0);
  }
  return schedules.value;
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

const getCoachName = (coachId) => {
  const coach = coaches.value.find((c) => c.coach_id === coachId);
  return coach ? coach.full_name : 'Unknown';
};

const bookSession = async (scheduleId) => {
  if (!user.value?.customer_id) {
    error.value = 'Customer information not found';
    return;
  }

  bookingInProgress.value = scheduleId;
  error.value = '';

  try {
    await bookingsAPI.create({
      customer_id: user.value.customer_id,
      schedule_id: scheduleId,
    });

    alert('Booking successful!');
    await loadSchedules();
  } catch (err) {
    console.error('Booking error:', err);
    error.value = err.response?.data?.detail || 'Failed to book session';
  } finally {
    bookingInProgress.value = null;
  }
};

const loadSchedules = async () => {
  try {
    loading.value = true;
    error.value = '';

    const [schedulesData, coachesData] = await Promise.all([
      schedulesAPI.getAll(),
      coachesAPI.getAll(),
    ]);

    schedules.value = schedulesData;
    coaches.value = coachesData;
  } catch (err) {
    console.error('Error loading schedules:', err);
    error.value = 'Failed to load schedules';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadSchedules();
});
</script>

<style scoped>
.schedule-view {
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
  margin-bottom: 2rem;
}

.loading,
.error-message,
.no-data {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error-message {
  background: #fee;
  color: #c33;
  border-radius: 5px;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.filter-btn {
  padding: 0.7rem 1.5rem;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.filter-btn:hover {
  background: #667eea;
  color: white;
}

.filter-btn.active {
  background: #667eea;
  color: white;
}

.schedules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.schedule-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.schedule-card:hover {
  transform: translateY(-5px);
}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.schedule-header h3 {
  color: #333;
  font-size: 1.5rem;
  margin: 0;
}

.status-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
}

.status-badge.available {
  background: #d4edda;
  color: #155724;
}

.status-badge.full {
  background: #f8d7da;
  color: #721c24;
}

.schedule-details {
  margin-bottom: 1.5rem;
}

.detail-item {
  margin-bottom: 0.8rem;
  color: #555;
}

.detail-item strong {
  color: #333;
}

.btn-book {
  width: 100%;
  padding: 0.8rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-book:hover:not(:disabled) {
  transform: scale(1.02);
}

.btn-book:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-prompt {
  text-align: center;
  padding: 0.8rem;
  background: #f0f0f0;
  border-radius: 5px;
}

.login-prompt a {
  color: #667eea;
  font-weight: 600;
  text-decoration: none;
}

.login-prompt a:hover {
  text-decoration: underline;
}
</style>
