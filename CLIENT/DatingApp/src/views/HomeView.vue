<template>
  <div class="home-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>Welcome to Your Dating App</h1>
        <p>Find your perfect match today</p>
        <div class="cta-buttons">
          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/auth" 
            class="cta-button primary"
          >
            Get Started
          </router-link>
          <router-link 
            v-else 
            to="/discover" 
            class="cta-button primary"
          >
            Discover Matches
          </router-link>
          <router-link 
            v-if="!authStore.isAuthenticated" 
            to="/auth" 
            class="cta-button secondary"
          >
            Login
          </router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="@/assets/dating-hero.png" alt="Happy couple" />
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2>Why Choose Our App</h2>
      <div class="feature-cards">
        <div class="feature-card">
          <div class="feature-icon">💖</div>
          <h3>Smart Matching</h3>
          <p>Our advanced algorithm finds compatible partners based on your interests and personality.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🔒</div>
          <h3>Secure Dating</h3>
          <p>Your safety is our priority with verified profiles and secure messaging.</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌎</div>
          <h3>Global Community</h3>
          <p>Connect with singles from all over the world.</p>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="testimonials" v-if="!authStore.isAuthenticated">
      <h2>Success Stories</h2>
      <div class="testimonial-cards">
        <div class="testimonial-card">
          <img src="@/assets/user1.jpg" alt="Happy couple" class="testimonial-image" />
          <p>"We met on this app and have been together for 2 years now!"</p>
          <span>- Alex & Taylor</span>
        </div>
        <div class="testimonial-card">
          <img src="@/assets/user2.jpg" alt="Happy couple" class="testimonial-image" />
          <p>"The matching system really understands what I was looking for."</p>
          <span>- Jordan</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import NavBar from '@/components/common/NavBar.vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Hero Section Styles */
.hero {
  display: flex;
  align-items: center;
  gap: 40px;
  margin-bottom: 60px;
  padding: 40px 0;
}

.hero-content {
  flex: 1;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #2c3e50;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 30px;
  color: #7f8c8d;
}

.cta-buttons {
  display: flex;
  gap: 15px;
}

.cta-button {
  padding: 12px 24px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.cta-button.primary {
  background-color: #4a89dc;
  color: white;
}

.cta-button.primary:hover {
  background-color: #3a70c2;
}

.cta-button.secondary {
  border: 1px solid #4a89dc;
  color: #4a89dc;
}

.cta-button.secondary:hover {
  background-color: #f5f9ff;
}

.hero-image {
  flex: 1;
}

.hero-image img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

/* Features Section */
.features {
  margin: 80px 0;
}

.features h2 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2rem;
  color: #2c3e50;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  padding: 30px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.feature-card p {
  color: #7f8c8d;
  line-height: 1.6;
}

/* Testimonials */
.testimonials {
  margin: 80px 0;
}

.testimonials h2 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2rem;
  color: #2c3e50;
}

.testimonial-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.testimonial-card {
  padding: 30px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.testimonial-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 20px;
  display: block;
}

.testimonial-card p {
  font-style: italic;
  margin-bottom: 15px;
  color: #7f8c8d;
}

.testimonial-card span {
  font-weight: 500;
  color: #2c3e50;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    flex-direction: column;
  }
  
  .hero-content, .hero-image {
    text-align: center;
  }
  
  .cta-buttons {
    justify-content: center;
  }
}
</style>