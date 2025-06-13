<script setup>
import { onMounted, ref } from 'vue';
import userImage from '@/assets/user.png';
import ProfileForm from '@/components/auth/ProfileForm.vue';
import api from '@/composables/apiConnection';

const userProfile = ref(null);
const isLoading = ref(false);
const isEditing = ref(false);
const error = ref(null);
const selectedFile = ref(null);
const isUploading = ref(false);

const fetchProfile = async () => {
  try {
    isLoading.value = true;
    const response = await api.get('/user/profile');
    const data = response.data;

    if (data.profile) {
      // Combine first and last name into a single string
      const name = `${data.profile.first_name || ''} ${data.profile.last_name || ''}`.trim();

      // Find primary photo URL if exists
      const primaryPhoto = data.photos?.find(p => p.is_primary)?.url || '';

      userProfile.value = {
        name,
        age: data.profile.age,
        location: data.profile.location,
        bio: data.profile.bio,
        gender: data.profile.gender,
        interested_in: data.profile.interested_in,
        birth_date: data.profile.birth_date,
        profile_picture: primaryPhoto,
        photos: data.photos || []
      };
    } else {
      userProfile.value = null;
    }
  } catch (err) {
    console.error('Fetch error:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to load profile';
  } finally {
    isLoading.value = false;
  }
};

const handleSave = async (updatedProfile) => {
  try {
    isLoading.value = true;

    // split name into first and last
    const [first_name, ...last_nameParts] = (updatedProfile.name || '').split(' ');
    const last_name = last_nameParts.join(' ');

    const payload = {
      first_name,
      last_name,
      gender: updatedProfile.gender,
      interested_in: updatedProfile.interested_in,
      birth_date: updatedProfile.birth_date,
      bio: updatedProfile.bio,
      location: updatedProfile.location,
    };

    await api.put('/user/profile', payload);

    // After successful save, fetch profile again to refresh data
    await fetchProfile();

    isEditing.value = false;
  } catch (err) {
    console.error('Save error:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to update profile';
  } finally {
    isLoading.value = false;
  }
};

const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadPhoto = async () => {
  if (!selectedFile.value) return;

  try {
    isUploading.value = true;
    const formData = new FormData();
    formData.append('photo', selectedFile.value);

    await api.post('/user/photos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    await fetchProfile();
    selectedFile.value = null;
  } catch (err) {
    console.error('Upload error:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to upload photo';
  } finally {
    isUploading.value = false;
  }
};

const setPrimaryPhoto = async (photoId) => {
  try {
    isLoading.value = true;
    await api.put(`/user/photos/${photoId}/primary`);
    await fetchProfile();
  } catch (err) {
    console.error('Set primary error:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to set primary photo';
  } finally {
    isLoading.value = false;
  }
};

const deletePhoto = async (photoId) => {
  try {
    isLoading.value = true;
    await api.delete(`/user/photos/${photoId}/delete`);
    await fetchProfile();
  } catch (err) {
    console.error('Delete error:', err);
    error.value = err.response?.data?.message || err.message || 'Failed to delete photo';
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchProfile();
});
</script>

<template>
  <div class="profile-view">
    <div v-if="isLoading && !userProfile" class="loading">Loading your profile...</div>

    <div v-else-if="error" class="error">{{ error }}</div>

    <div v-else>
      <div class="profile-header">
        <h1>Your Profile</h1>
        <button @click="isEditing = !isEditing" class="edit-btn">
          {{ isEditing ? 'Cancel' : 'Edit Profile' }}
        </button>
      </div>

      <ProfileForm
        v-if="isEditing"
        :profile="userProfile"
        @save="handleSave"
        @cancel="isEditing = false"
      />

      <div v-else class="profile-display">
        <div class="profile-image">
          <img
            :src="userProfile?.photo || userImage"
            :alt="userProfile?.name || 'User'"
          />
          
          <div class="photo-upload">
            <input 
              type="file" 
              accept="image/*" 
              @change="handleFileSelect"
              id="photo-upload"
              style="display: none"
            />
            <label for="photo-upload" class="upload-btn">Choose Photo</label>
            <button 
              @click="uploadPhoto" 
              :disabled="!selectedFile || isUploading"
              class="upload-btn"
            >
              {{ isUploading ? 'Uploading...' : 'Upload' }}
            </button>
          </div>

          <div v-if="userProfile?.photos?.length > 0" class="photo-gallery">
            <h3>Your Photos</h3>
            <div class="photos">
              <div v-for="photo in userProfile.photos" :key="photo.id" class="photo-item">
                <img :src="photo.url" alt="User photo" />
                <div class="photo-actions">
                  <button 
                    @click="setPrimaryPhoto(photo.id)" 
                    :disabled="photo.is_primary"
                    class="photo-btn"
                  >
                    {{ photo.is_primary ? 'Primary' : 'Set Primary' }}
                  </button>
                  <button 
                    @click="deletePhoto(photo.id)" 
                    class="photo-btn delete"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="profile-details">
          <h2>{{ userProfile?.name }}, {{ userProfile?.age }}</h2>
          
          <p><strong>Gender:</strong> {{ userProfile?.gender || 'Not specified' }}</p>
          <p><strong>Interested In:</strong> {{ userProfile?.interested_in || 'Not specified' }}</p>
          <p><strong>Birth Date:</strong> {{ userProfile?.birth_date ? new Date(userProfile.birth_date).toLocaleDateString() : 'Not specified' }}</p>

          <p class="location"><strong>Location:</strong> {{ userProfile?.location }}</p>
          <p class="bio"><strong>Bio:</strong> {{ userProfile?.bio }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.edit-btn {
  background-color: #4a89dc;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.profile-display {
  display: flex;
  gap: 2rem;
}

.profile-image {
  flex: 0 0 300px;
}

.profile-image img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.profile-details {
  flex: 1;
}

h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
}

.location {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
}

.bio {
  margin: 0 0 2rem 0;
  line-height: 1.6;
  font-size: 1.1rem;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: #e74c3c;
}

.photo-upload {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
}

.upload-btn {
  background-color: #4a89dc;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-align: center;
}

.upload-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.photo-gallery {
  margin-top: 2rem;
}

.photo-gallery h3 {
  margin-bottom: 1rem;
}

.photos {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.photo-item {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.5rem;
}

.photo-item img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.photo-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.photo-btn {
  flex: 1;
  padding: 0.3rem;
  font-size: 0.8rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 3px;
  cursor: pointer;
}

.photo-btn:disabled {
  background-color: #4a89dc;
  color: white;
  cursor: default;
}

.photo-btn.delete {
  background-color: #e74c3c;
  color: white;
}
</style>