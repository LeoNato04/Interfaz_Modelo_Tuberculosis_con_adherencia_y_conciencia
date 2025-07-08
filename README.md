# Modelo_SEIR_Tuberculosis
Simulación compartimental de tuberculosis (TB) con 6 estados poblacionales. Incluye formulación matemática, análisis cualitativo, cálculo de 𝑅_𝑏, simulador web interactivo, análisis de sensibilidad en 3D y documentación LaTeX. Contexto: Malakand, Pakistán.  Herramientas: Python, Chart.js, HTML/JS, LaTeX.


# Modelo Compartimental de Tuberculosis

Este repositorio contiene la implementación de un modelo compartimental para simular la dinámica de la tuberculosis (TB) en una población. El modelo divide la población en seis estados: susceptibles, expuestos (latentes), infectados activos no diagnosticados, en tratamiento con alta o baja adherencia, y recuperados.

Incluye:

- Formulación matemática detallada del sistema de EDOs  
- Análisis cualitativo (no negatividad, región invariante)  
- Cálculo del número reproductivo básico \( R_b \)  
- Simulación interactiva vía interfaz web (HTML + JS)  
- Análisis de sensibilidad con visualizaciones 3D
- Documento explicativo en formato LaTeX  

Aplicación contextual: Región de Malakand, Pakistán  
Herramientas usadas: Python (simulación), Chart.js (gráficos), HTML/CSS/JS (interfaz), LaTeX (documentación)


## Instrucciones de Uso
Sigue estos pasos para ejecutar la simulación localmente en tu máquina:

### 1. Clona este repositorio
git clone https://github.com/LeoNato04/Modelo_SEIR_Tuberculosis

### 2. Crea un entorno virtual
```bash
python -m venv venv
```

### 3. Activa el entorno virtual
#### En Windows:
```bash
venv\Scripts\activate
```
#### En macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Instala las dependencias necesarias
```bash
pip install flask numpy scipy
```

### 5. Ejecuta la aplicación
```bash
python app.py
```

### 6. Abre tu navegador
Ingresa a http://localhost:5000 para interactuar con la simulación.

👨‍💻 Desarrollado por: Leonel Fortunato Lizarbe Almeyda
leonel.lizarbe@unmsm.edu.pe


