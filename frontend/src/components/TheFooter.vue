<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-section">
          <h3>FitLife</h3>
          <p>Your Path to Fitness Excellence</p>
        </div>
        <div class="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="#about">About</a></li>
            <li><a href="#gallery">Gallery</a></li>
            <li><a href="#memberships">Memberships</a></li>
          </ul>
        </div>
        <div class="footer-section">
          <h3>Contact</h3>
          <p>Str. Mykoly Pymonenka 18</p>
          <p>+380991267075</p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2025 FitLife. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer {
  background: #2c3e50;
  color: white;
  padding: 3rem 0 1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 2rem;
}

.footer-section h3 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
  text-transform: uppercase;
}

.footer-section p {
  color: #bdc3c7;
  line-height: 1.6;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  color: #bdc3c7;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid #34495e;
  padding-top: 1rem;
  text-align: center;
  color: #95a5a6;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
