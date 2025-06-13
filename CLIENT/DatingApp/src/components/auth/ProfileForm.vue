<script setup>
import { ref, watch, toRefs } from 'vue';

const props = defineProps({
  profile: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['save', 'cancel']);

const form = ref({
  name: '',
  gender: '',
  interested_in: '',
  birth_date: '',
  bio: '',
  location: ''
});

// Populate form when profile prop changes
watch(() => props.profile, (newProfile) => {
  if (newProfile) {
    form.value = {
      name: newProfile.name || '',
      gender: newProfile.gender || '',
      interested_in: newProfile.interested_in || '',
      birth_date: newProfile.birth_date || '',
      bio: newProfile.bio || '',
      location: newProfile.location || ''
    };
  }
}, { immediate: true });

const onSave = () => {
  emit('save', { ...form.value });
};

const onCancel = () => {
  emit('cancel');
};
</script>

<template>
  <form @submit.prevent="onSave" class="profile-form">
    <div>
      <label for="name">Full Name</label>
      <input id="name" v-model="form.name" type="text" required />
    </div>

    <div>
      <label for="gender">Gender</label>
      <select id="gender" v-model="form.gender">
        <option value="">Select gender</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
    </div>

    <div>
      <label for="interested_in">Interested In</label>
      <select id="interested_in" v-model="form.interested_in">
        <option value="">Select</option>
        <option>Men</option>
        <option>Women</option>
        <option>Everyone</option>
      </select>
    </div>

    <div>
      <label for="birth_date">Birth Date</label>
      <input id="birth_date" v-model="form.birth_date" type="date" />
    </div>

    <div>
      <label for="location">Location</label>
      <input id="location" v-model="form.location" type="text" />
    </div>

    <div>
      <label for="bio">Bio</label>
      <textarea id="bio" v-model="form.bio" rows="4" />
    </div>
    

    <div class="buttons">
      <button type="submit">Save</button>
      <button type="button" @click="onCancel">Cancel</button>
    </div>
  </form>
</template>

<style scoped>
.profile-form div {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

input, select, textarea {
  width: 100%;
  padding: 0.4rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.buttons {
    display: flex;
    
}


button {
  background-color: #4a89dc;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 3px;
}

</style>
