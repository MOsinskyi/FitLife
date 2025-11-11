<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="brand-name">FitLife</h1>
        <p class="tagline">Your Path to Fitness Excellence</p>
        <button class="btn-register">Register for a Session</button>
      </div>
    </section>

    <!-- Why We're Best Section -->
    <section id="why-best" class="section why-best">
      <div class="container">
        <h2>Why We're the Best</h2>
        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="star-icon">⭐</div>
            <h3>Advantage</h3>
            <p>Join a large club with extensive facilities, extensive description of why this is great, top-notch equipment, and a supportive community</p>
          </div>
          <div class="benefit-card">
            <div class="star-icon">⭐</div>
            <h3>Advantage</h3>
            <p>Join a large club with extensive facilities, extensive description of why this is great, top-notch equipment, and a supportive community</p>
          </div>
          <div class="benefit-card">
            <div class="star-icon">⭐</div>
            <h3>Advantage</h3>
            <p>Join a large club with extensive facilities, extensive description of why this is great, top-notch equipment, and a supportive community</p>
          </div>
        </div>
      </div>
    </section>

    <!-- About Us Section -->
    <section id="about" class="section about">
      <div class="container">
        <h2>About Us</h2>
        <div class="about-content">
          <p class="about-description">
            Our office description, our trainers, how we work, the best description, the best our office,
            what we have, what we can, such description, such description.
          </p>
        </div>
      </div>
    </section>

    <!-- Gallery Section -->
    <section id="gallery" class="section gallery">
      <div class="container">
        <h2>Gallery</h2>
        <div class="gallery-grid">
          <div class="gallery-item"></div>
          <div class="gallery-item"></div>
          <div class="gallery-item"></div>
          <div class="gallery-item"></div>
          <div class="gallery-item"></div>
          <div class="gallery-item"></div>
        </div>
      </div>
    </section>

    <!-- Zones and Services Section -->
    <section id="zones-services" class="section zones-services">
      <div class="container">
        <h2>Zones and Services</h2>
        <div class="zones-services-grid">
          <div class="zones-list">
            <h3>Zones</h3>
            <ul>
              <li>Zone 1</li>
              <li>Zone 2</li>
              <li>Zone 3</li>
              <li>Zone 4</li>
              <li>Zone 5</li>
            </ul>
          </div>
          <div class="services-list">
            <h3>Services</h3>
            <ul>
              <li>Service 1</li>
              <li>Service 2</li>
              <li>Service 3</li>
              <li>Service 4</li>
              <li>Service 5</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Reviews Section -->
    <section id="reviews" class="section reviews">
      <div class="container">
        <h2>Reviews</h2>
        <div class="reviews-grid">
          <div class="review-card">
            <div class="star-badge">⭐</div>
            <p class="client-type">For Client</p>
            <p class="review-text">Join an excellent beautiful club for our good office</p>
            <div class="stars">★★★★★</div>
          </div>
          <div class="review-card">
            <div class="star-badge">⭐</div>
            <p class="client-type">For Client</p>
            <p class="review-text">Join an excellent beautiful club for our good office</p>
            <div class="stars">★★★★★</div>
          </div>
          <div class="review-card">
            <div class="star-badge">⭐</div>
            <p class="client-type">For Client</p>
            <p class="review-text">Join an excellent beautiful club for our good office</p>
            <div class="stars">★★★★★</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Our Trainers Section -->
    <section id="trainers" class="section trainers">
      <div class="container">
        <h2>Our Trainers</h2>
        <div class="trainers-grid">
          <div class="trainer-card">
            <div class="trainer-image"></div>
            <h3>Name Surname</h3>
            <p>Short coaching experience just a couple of lines</p>
          </div>
          <div class="trainer-card">
            <div class="trainer-image"></div>
            <h3>Name Surname</h3>
            <p>Short coaching experience just a couple of lines</p>
          </div>
          <div class="trainer-card">
            <div class="trainer-image"></div>
            <h3>Name Surname</h3>
            <p>Short coaching experience just a couple of lines</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Schedule Section -->
    <section id="schedule" class="section schedule">
      <div class="container">
        <h2>Schedule</h2>
        <div class="schedule-placeholder">
          <p>Training schedule and booking system</p>
          <router-link to="/schedule" class="btn-view-schedule">View Full Schedule</router-link>
        </div>
      </div>
    </section>

    <!-- Memberships Section -->
    <section id="memberships" class="section memberships">
      <div class="container">
        <h2>Memberships</h2>
        <div class="memberships-grid">
          <div class="membership-card">
            <div class="membership-image"></div>
            <h3>Name</h3>
            <ul class="membership-includes">
              <li>Includes 1</li>
              <li>Includes 2</li>
              <li>Includes 3</li>
              <li>Includes 4</li>
            </ul>
          </div>
          <div class="membership-card">
            <div class="membership-image"></div>
            <h3>Name</h3>
            <ul class="membership-includes">
              <li>Includes 1</li>
              <li>Includes 2</li>
              <li>Includes 3</li>
              <li>Includes 4</li>
            </ul>
          </div>
          <div class="membership-card">
            <div class="membership-image"></div>
            <h3>Name</h3>
            <ul class="membership-includes">
              <li>Includes 1</li>
              <li>Includes 2</li>
              <li>Includes 3</li>
              <li>Includes 4</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Price Section -->
    <section id="price" class="section price">
      <div class="container">
        <h2>Price</h2>
        <div class="price-content">
          <p class="price-description">Information about pricing and payment options</p>
        </div>
      </div>
    </section>

    <!-- Booking Section -->
    <section id="booking" class="section booking">
      <div class="container">
        <h2>Where to Find Us?</h2>
        <div class="booking-content">
          <div class="contact-info">
            <h3>Address</h3>
            <p>Str. Mykoly Pymonenka 18</p>

            <h3>Contact</h3>
            <p>+380991267075</p>

            <h3>Price</h3>
            <p>From 500 UAH</p>

            <h3>Social Media</h3>
            <div class="social-links">
              <span class="social-icon">★</span>
              <span class="social-icon">★</span>
              <span class="social-icon">★</span>
            </div>
          </div>
          <div class="booking-form">
            <h3>Book Your First Session</h3>
            <form @submit.prevent="handleBooking">
              <input type="tel" placeholder="Enter your phone number" class="form-input" v-model="phoneNumber">
              <button type="submit" class="btn-book">Book</button>
            </form>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const phoneNumber = ref('');

const handleBooking = () => {
  if (phoneNumber.value) {
    alert(`Booking request submitted for: ${phoneNumber.value}`);
    phoneNumber.value = '';
  }
};
</script>

<style scoped>
.home {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #8b9198 0%, #6d757d 100%);
  color: white;
  padding: 120px 20px;
  text-align: center;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content {
  max-width: 800px;
}

.brand-name {
  font-size: 4rem;
  margin-bottom: 1rem;
  font-weight: bold;
  letter-spacing: 2px;
}

.tagline {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  font-weight: 300;
}

.btn-register {
  background: #5a6268;
  color: white;
  padding: 15px 40px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-register:hover {
  background: #4a5258;
}

/* Section Styling */
.section {
  padding: 80px 20px;
}

.section:nth-child(even) {
  background: #e9ecef;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section h2 {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #333;
  text-transform: uppercase;
}

/* Why We're Best Section */
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
}

.benefit-card {
  text-align: center;
  padding: 2rem;
}

.star-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.benefit-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
  text-transform: uppercase;
}

.benefit-card p {
  color: #666;
  line-height: 1.6;
}

/* About Section */
.about-content {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
}

.about-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.8;
}

/* Gallery Section */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.gallery-item {
  background: #d3d3d3;
  aspect-ratio: 1;
  position: relative;
}

.gallery-item::before,
.gallery-item::after {
  content: '';
  position: absolute;
  background: #999;
}

.gallery-item::before {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  transform: rotate(45deg);
  transform-origin: top left;
}

.gallery-item::after {
  top: 0;
  right: 0;
  width: 100%;
  height: 2px;
  transform: rotate(-45deg);
  transform-origin: top right;
}

/* Zones and Services Section */
.zones-services-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4rem;
  max-width: 800px;
  margin: 0 auto;
}

.zones-list h3,
.services-list h3 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.zones-list ul,
.services-list ul {
  list-style: none;
  padding: 0;
}

.zones-list li,
.services-list li {
  padding: 0.5rem 0;
  color: #666;
  border-bottom: 1px solid #ddd;
}

/* Reviews Section */
.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.review-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.star-badge {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.client-type {
  font-weight: 600;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.review-text {
  color: #666;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.stars {
  color: #333;
  font-size: 1.5rem;
  letter-spacing: 0.25rem;
}

/* Trainers Section */
.trainers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
}

.trainer-card {
  text-align: center;
}

.trainer-image {
  background: #d3d3d3;
  aspect-ratio: 3/4;
  margin-bottom: 1rem;
  position: relative;
}

.trainer-image::before,
.trainer-image::after {
  content: '';
  position: absolute;
  background: #999;
}

.trainer-image::before {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  transform: rotate(45deg);
  transform-origin: top left;
}

.trainer-image::after {
  top: 0;
  right: 0;
  width: 100%;
  height: 2px;
  transform: rotate(-45deg);
  transform-origin: top right;
}

.trainer-card h3 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #333;
  text-transform: uppercase;
}

.trainer-card p {
  color: #666;
  line-height: 1.6;
}

/* Schedule Section */
.schedule-placeholder {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 10px;
}

.schedule-placeholder p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
}

.btn-view-schedule {
  display: inline-block;
  background: #5a6268;
  color: white;
  padding: 12px 30px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-view-schedule:hover {
  background: #4a5258;
}

/* Memberships Section */
.memberships-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
}

.membership-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.membership-image {
  background: #d3d3d3;
  aspect-ratio: 16/9;
  margin-bottom: 1.5rem;
  position: relative;
}

.membership-image::before,
.membership-image::after {
  content: '';
  position: absolute;
  background: #999;
}

.membership-image::before {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  transform: rotate(45deg);
  transform-origin: top left;
}

.membership-image::after {
  top: 0;
  right: 0;
  width: 100%;
  height: 2px;
  transform: rotate(-45deg);
  transform-origin: top right;
}

.membership-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
  text-transform: uppercase;
}

.membership-includes {
  list-style: none;
  padding: 0;
}

.membership-includes li {
  padding: 0.5rem 0;
  color: #666;
  border-bottom: 1px solid #eee;
}

/* Price Section */
.price-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.price-description {
  font-size: 1.1rem;
  color: #666;
  line-height: 1.8;
}

/* Booking Section */
.booking-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 4rem;
  max-width: 900px;
  margin: 0 auto;
}

.contact-info h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  margin-top: 1.5rem;
  color: #333;
  text-transform: uppercase;
}

.contact-info h3:first-child {
  margin-top: 0;
}

.contact-info p {
  color: #666;
  margin-bottom: 1rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-icon {
  font-size: 2rem;
  color: #333;
}

.booking-form {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
}

.booking-form h3 {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  color: #333;
  text-transform: uppercase;
}

.form-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.btn-book {
  width: 100%;
  background: #5a6268;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-book:hover {
  background: #4a5258;
}

@media (max-width: 768px) {
  .brand-name {
    font-size: 2.5rem;
  }

  .benefits-grid,
  .reviews-grid,
  .trainers-grid,
  .memberships-grid {
    grid-template-columns: 1fr;
  }

  .zones-services-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .booking-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
