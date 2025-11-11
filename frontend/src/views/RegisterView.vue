<template>
  <div class="register-container">
    <div class="register-card">
      <h1>FitLife</h1>
      <h2>Create Account</h2>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="success" class="success-message">
        Account created successfully! Redirecting to login...
      </div>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="role">I want to register as:</label>
          <select id="role" v-model="role" required>
            <option value="customer">Customer</option>
            <option value="coach">Coach</option>
          </select>
        </div>

        <div class="form-group">
          <label for="fullName">Full Name</label>
          <input
            id="fullName"
            v-model="fullName"
            type="text"
            placeholder="Enter your full name"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your email"
            required
          />
        </div>

        <div class="form-group">
          <label for="phone">Phone</label>
          <input
            id="phone"
            v-model="phone"
            type="tel"
            placeholder="Enter your phone number"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <div v-if="role === 'coach'" class="form-group">
          <label for="specialization">Specialization</label>
          <input
            id="specialization"
            v-model="specialization"
            type="text"
            placeholder="e.g., Yoga, Strength Training"
            required
          />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <div class="login-link">
        <p>Already have an account? <router-link to="/login">Login here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { customersAPI, coachesAPI, usersAPI } from '../services/api';

const router = useRouter();

const role = ref('customer');
const fullName = ref('');
const email = ref('');
const phone = ref('');
const password = ref('');
const specialization = ref('');
const loading = ref(false);
const error = ref('');
const success = ref(false);

const handleRegister = async () => {
  loading.value = true;
  error.value = '';
  success.value = false;

  try {
    if (role.value === 'customer') {
      await customersAPI.create({
        full_name: fullName.value,
        email: email.value,
        phone: phone.value,
        password: password.value,
      });
    } else if (role.value === 'coach') {
      await coachesAPI.create({
        full_name: fullName.value,
        email: email.value,
        phone: phone.value,
        specialization: specialization.value,
        password: password.value,
      });
    }

    success.value = true;
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (err) {
    console.error('Registration error:', err);
    error.value = err.response?.data?.detail || 'Registration failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 450px;
}

h1 {
  text-align: center;
  color: #667eea;
  margin-bottom: 10px;
  font-size: 2.5rem;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 1.5rem;
  font-weight: 400;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
  text-align: center;
}

.success-message {
  background: #efe;
  color: #3c3;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

input,
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus,
select:focus {
  outline: none;
  border-color: #667eea;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  margin-top: 20px;
  text-align: center;
}

.login-link p {
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
