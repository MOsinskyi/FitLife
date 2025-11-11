<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1>Welcome, {{ user?.full_name }}</h1>
        <p class="role-badge">Coach Dashboard</p>
        <p v-if="user?.specialization" class="specialization">
          Specialization: {{ user.specialization }}
        </p>
      </div>

      <div class="dashboard-grid">
        <div class="card stats-card">
          <h2>Quick Stats</h2>
          <div class="stats">
            <div class="stat-item">
              <div class="stat-value">{{ mySchedules.length }}</div>
              <div class="stat-label">My Sessions</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ totalBookings }}</div>
              <div class="stat-label">Total Bookings</div>
            </div>
          </div>
        </div>

        <div class="card create-schedule-card">
          <h2>Create New Schedule</h2>
          <form @submit.prevent="createSchedule" class="schedule-form">
            <div class="form-group">
              <label>Training Type</label>
              <input v-model="newSchedule.training_type" type="text" required />
            </div>
            <div class="form-group">
              <label>Date</label>
              <input v-model="newSchedule.date" type="date" required />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Start Time</label>
                <input v-model="newSchedule.start_time" type="time" required />
              </div>
              <div class="form-group">
                <label>End Time</label>
                <input v-model="newSchedule.end_time" type="time" required />
              </div>
            </div>
            <div class="form-group">
              <label>Capacity</label>
              <input v-model.number="newSchedule.capacity" type="number" min="1" required />
            </div>
            <button type="submit" class="btn-create" :disabled="creating">
              {{ creating ? 'Creating...' : 'Create Schedule' }}
            </button>
          </form>
        </div>

        <div class="card full-width">
          <h2>My Training Sessions</h2>
          <div v-if="loadingSchedules" class="loading">Loading...</div>
          <div v-else-if="mySchedules.length === 0" class="no-data">
            No sessions created yet. Create your first schedule above!
          </div>
          <div v-else class="schedules-list">
            <div
              v-for="schedule in mySchedules"
              :key="schedule.schedule_id"
              class="schedule-item"
            >
              <div class="schedule-info">
                <h3>{{ schedule.training_type }}</h3>
                <p>{{ formatDate(schedule.date) }}</p>
                <p>{{ schedule.start_time }} - {{ schedule.end_time }}</p>
                <p>
                  Capacity: {{ schedule.capacity }} spots available
                </p>
              </div>
              <div class="schedule-actions">
                <button
                  @click="viewBookings(schedule.schedule_id)"
                  class="btn-view"
                >
                  View Bookings ({{ getBookingsCount(schedule.schedule_id) }})
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedScheduleBookings" class="card full-width">
          <h2>Bookings for Selected Session</h2>
          <button @click="selectedScheduleBookings = null" class="btn-close">Close</button>
          <div v-if="selectedScheduleBookings.length === 0" class="no-data">
            No bookings for this session yet.
          </div>
          <div v-else class="bookings-list">
            <div
              v-for="booking in selectedScheduleBookings"
              :key="booking.booking_id"
              class="booking-item"
            >
              <div class="booking-info">
                <h4>Customer ID: {{ booking.customer_id }}</h4>
                <p>Booking ID: {{ booking.booking_id }}</p>
                <p>Status: <span class="status">{{ booking.status }}</span></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { schedulesAPI, bookingsAPI } from '../services/api';
import { useAuth } from '../composables/useAuth';

const { user } = useAuth();

const mySchedules = ref([]);
const allBookings = ref([]);
const loadingSchedules = ref(true);
const creating = ref(false);
const selectedScheduleBookings = ref(null);

const newSchedule = ref({
  training_type: '',
  date: '',
  start_time: '',
  end_time: '',
  capacity: 10,
});

const totalBookings = computed(() => {
  return allBookings.value.length;
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

const getBookingsCount = (scheduleId) => {
  return allBookings.value.filter((b) => b.schedule_id === scheduleId).length;
};

const createSchedule = async () => {
  if (!user.value?.coach_id) {
    alert('Coach information not found');
    return;
  }

  creating.value = true;

  try {
    await schedulesAPI.create({
      coach_id: user.value.coach_id,
      training_type: newSchedule.value.training_type,
      date: newSchedule.value.date,
      start_time: newSchedule.value.start_time,
      end_time: newSchedule.value.end_time,
      capacity: newSchedule.value.capacity,
    });

    alert('Schedule created successfully!');
    newSchedule.value = {
      training_type: '',
      date: '',
      start_time: '',
      end_time: '',
      capacity: 10,
    };

    await loadSchedules();
  } catch (error) {
    console.error('Create schedule error:', error);
    alert(error.response?.data?.detail || 'Failed to create schedule');
  } finally {
    creating.value = false;
  }
};

const viewBookings = async (scheduleId) => {
  try {
    const bookings = await bookingsAPI.getBySchedule(scheduleId);
    selectedScheduleBookings.value = bookings;
  } catch (error) {
    console.error('Error loading bookings:', error);
    alert('Failed to load bookings');
  }
};

const loadSchedules = async () => {
  try {
    loadingSchedules.value = true;
    const [schedulesData, bookingsData] = await Promise.all([
      schedulesAPI.getAll(),
      bookingsAPI.getAll(),
    ]);

    mySchedules.value = schedulesData.filter(
      (s) => s.coach_id === user.value?.coach_id
    );
    allBookings.value = bookingsData;
  } catch (error) {
    console.error('Error loading schedules:', error);
  } finally {
    loadingSchedules.value = false;
  }
};

onMounted(() => {
  loadSchedules();
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
  margin-bottom: 0.3rem;
}

.specialization {
  color: #666;
  font-style: italic;
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

.card.full-width {
  grid-column: 1 / -1;
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
  padding: 1.5rem;
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

.schedule-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
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

.loading,
.no-data {
  text-align: center;
  color: #666;
  padding: 2rem 0;
}

.schedules-list,
.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.schedule-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.schedule-info h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.schedule-info p {
  color: #666;
  margin-bottom: 0.3rem;
  font-size: 0.95rem;
}

.btn-view {
  padding: 0.6rem 1.2rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.btn-view:hover {
  background: #5568d3;
}

.btn-close {
  padding: 0.5rem 1rem;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 1rem;
}

.btn-close:hover {
  background: #5a6268;
}

.booking-item {
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.booking-info h4 {
  color: #333;
  margin-bottom: 0.5rem;
}

.booking-info p {
  color: #666;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
}

.status {
  font-weight: 600;
  text-transform: capitalize;
  color: #28a745;
}
</style>
