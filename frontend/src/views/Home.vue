<template>
  <div class="home">
    <h1>Welcome to Vocab App</h1>
    <p>Your vocabulary learning companion</p>
    <div class="actions">
      <router-link to="/login" class="btn">Get Started</router-link>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
  padding: 2rem;
}

h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #42b883;
}

p {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  background: #42b883;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background 0.3s;
}

.btn:hover {
  background: #35a372;
}
</style>
