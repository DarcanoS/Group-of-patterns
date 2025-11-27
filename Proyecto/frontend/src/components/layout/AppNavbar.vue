<template>
  <nav class="nav">
    <h1>Air Quality Plataforma</h1>

    <div>
      <router-link to="/">inicio</router-link>
      <router-link to="/login">Ingresar</router-link>
    </div>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  justify-content: space-between;
  padding: 16px 32px;
  background: #020617;
}

a {
  color: white;
  margin-left: 16px;
  text-decoration: none;
}
</style>
