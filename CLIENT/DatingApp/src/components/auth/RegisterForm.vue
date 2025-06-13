<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const emit = defineEmits(['success', 'error']);
const authStore = useAuthStore();

const isSubmitting = ref(false);

const form = ref({
  first_name: '',
  last_name: '',
  gender: '',
  interested_in: '',
  birth_date: '',
  bio: '',
  location: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const errors = ref({
  first_name: '',
  last_name: '',
  gender: '',
  interested_in: '',
  birth_date: '',
  bio: '',
  location: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const genders = ['Male', 'Female', 'Other'];
const interests = ['Male', 'Female', 'Other', 'Everyone', 'No preference'];

const validateField = () => {
  errors.value.first_name = form.value.first_name.trim() ? '' : 'First name is required';
  errors.value.last_name = form.value.last_name.trim() ? '' : 'Last name is required';

  errors.value.gender = genders.includes(form.value.gender) ? '' : 'Please select a valid gender';
  errors.value.interested_in = form.value.interested_in ? '' : 'Please select who you are interested in';

  errors.value.birth_date = form.value.birth_date ? '' : 'Birth date is required';

  // bio and location can be optional, but you can require if needed:
  // errors.value.bio = form.value.bio.trim() ? '' : 'Bio is required';
  // errors.value.location = form.value.location.trim() ? '' : 'Location is required';

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  errors.value.email = form.value.email.trim()
    ? emailRegex.test(form.value.email)
      ? ''
      : 'Invalid email'
    : 'Email is required';

  errors.value.password = form.value.password.length >= 6 ? '' : 'Password must be at least 6 characters';
  errors.value.confirmPassword = form.value.password === form.value.confirmPassword ? '' : 'Passwords do not match';

  return !Object.values(errors.value).some(error => error !== '');
};

const handleSubmit = async () => {
  if (!validateField()) return;

  isSubmitting.value = true;

  try {
    await authStore.register({
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      gender: form.value.gender,
      interested_in: form.value.interested_in,
      birth_date: form.value.birth_date,
      bio: form.value.bio,
      location: form.value.location,
      email: form.value.email,
      password: form.value.password,
    });
    emit('success');
  } catch (error) {
    emit('error', error.response?.data?.message || 'Registration failed');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <form @submit.prevent="handleSubmit" class="register-form">
    <div class="form-group">
      <label for="first_name">First Name</label>
      <input v-model="form.first_name" id="first_name" required />
      <span class="error-text" v-if="errors.first_name">{{ errors.first_name }}</span>
    </div>

    <div class="form-group">
      <label for="last_name">Last Name</label>
      <input v-model="form.last_name" id="last_name" required />
      <span class="error-text" v-if="errors.last_name">{{ errors.last_name }}</span>
    </div>

    <div class="form-group">
      <label for="gender">Gender</label>
      <select v-model="form.gender" id="gender" required>
        <option disabled value="">Select gender</option>
        <option v-for="g in genders" :key="g" :value="g">{{ g }}</option>
      </select>
      <span class="error-text" v-if="errors.gender">{{ errors.gender }}</span>
    </div>

    <div class="form-group">
      <label for="interested_in">Interested In</label>
      <select v-model="form.interested_in" id="interested_in" required>
        <option disabled value="">Select</option>
        <option v-for="i in interests" :key="i" :value="i">{{ i }}</option>
      </select>
      <span class="error-text" v-if="errors.interested_in">{{ errors.interested_in }}</span>
    </div>

    <div class="form-group">
      <label for="birth_date">Birth Date</label>
      <input type="date" v-model="form.birth_date" id="birth_date" required />
      <span class="error-text" v-if="errors.birth_date">{{ errors.birth_date }}</span>
    </div>

    <div class="form-group">
      <label for="bio">Bio</label>
      <textarea v-model="form.bio" id="bio" rows="3"></textarea>
    </div>

    <div class="form-group">
      <label for="location">Location</label>
      <input v-model="form.location" id="location" />
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" v-model="form.email" id="email" required />
      <span class="error-text" v-if="errors.email">{{ errors.email }}</span>
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" v-model="form.password" id="password" required />
      <span class="error-text" v-if="errors.password">{{ errors.password }}</span>
    </div>

    <div class="form-group">
      <label for="confirmPassword">Confirm Password</label>
      <input type="password" v-model="form.confirmPassword" id="confirmPassword" required />
      <span class="error-text" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
    </div>

    <button type="submit" :disabled="isSubmitting" class="submit-btn">
      {{ isSubmitting ? 'Registering...' : 'Create Account' }}
    </button>
  </form>
</template>

<style scoped>
.register-form {
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

label {
  font-weight: 600;
  color: #333;
}

input,
select,
textarea {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #4a89dc;
}

.error-text {
  color: #e74c3c;
  font-size: 0.85rem;
}

.submit-btn {
  background-color: #4a89dc;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
