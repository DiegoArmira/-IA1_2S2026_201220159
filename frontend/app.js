document.getElementById('analizar').addEventListener('click', async () => {
  const sintoma = document.getElementById('sintoma').value;
  const severidad = document.getElementById('severidad').value;
  const output = document.getElementById('resultado');
  output.textContent = 'Consultando la base de conocimiento...';
  try {
    const response = await fetch(`/api/query?name=diagnostico&sintoma=${encodeURIComponent(sintoma)}`);
    const data = await response.json();
    output.textContent = `Severidad: ${severidad}\n${JSON.stringify(data, null, 2)}`;
  } catch (error) {
    output.textContent = `No fue posible consultar el backend: ${error.message}`;
  }
});
