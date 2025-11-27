<template>
  <section class="how-section">
    <div class="container">
      <h2>Como funciona la plataforma?</h2>

      <div class="steps">
        <div class="step">
          <h3>1. Recoleccion de datos</h3>
          <p>SLos sensores recolectan los datos en tiempo real.</p>
        </div>

        <div class="step">
          <h3>2. Procesan</h3>
          <p>Son procesados los sistemas de polucion.</p>
        </div>

        <div class="step">
          <h3>3. Visualizacion</h3>
          <p>Los usuarios ven los registros .</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.how-section {
  padding: 80px 20px;
  background: #0f172a;
  color: white;
  text-align: center;
}

.steps {
  display: flex;
  gap: 30px;
  justify-content: center;
  margin-top: 40px;
  flex-wrap: wrap;
}

.step {
  background: #1e293b;
  padding: 25px;
  border-radius: 12px;
  width: 260px;
  box-shadow: 0 0 10px rgba(0,0,0,.3);
}
</style>
