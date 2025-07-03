console.log("¡main.js cargado!");

function runSimulation(modoSimulacion = 1) {
    const params = {
        u: parseFloat(document.getElementById("u").value),
        n: parseFloat(document.getElementById("n").value),
        b: parseFloat(document.getElementById("b").value),
        c: parseFloat(document.getElementById("c").value),
        g: parseFloat(document.getElementById("g").value),
        h: parseFloat(document.getElementById("h").value),
        k: parseFloat(document.getElementById("k").value),
        r: parseFloat(document.getElementById("r").value),
        gamma: parseFloat(document.getElementById("gamma").value),
        p: parseFloat(document.getElementById("p").value),
        d1: parseFloat(document.getElementById("d1").value),
        d2: parseFloat(document.getElementById("d2").value),
        days: parseInt(document.getElementById("dayRange").value),
        modo: modoSimulacion 
    };

    fetch("/run_simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        if ('error' in data && data.error) return;

        renderChart2D(data, modoSimulacion);

        // Mostrar valores calculados en el panel derecho
        document.getElementById("betaDisplay").textContent = data.beta_efectivo?.toFixed(4) ?? "-";
        document.getElementById("rbDisplay").textContent = data.rb?.toFixed(4) ?? "-";

        const p = data.params_used || {};
        document.getElementById("a1Display").textContent = p.a1?.toFixed(3) ?? "-";
        document.getElementById("a2Display").textContent = p.a2?.toFixed(3) ?? "-";
        document.getElementById("m1Display").textContent = p.m1?.toFixed(3) ?? "-";
        document.getElementById("m2Display").textContent = p.m2?.toFixed(3) ?? "-";
        document.getElementById("z1Display").textContent = p.z1?.toFixed(4) ?? "-";
        document.getElementById("z2Display").textContent = p.z2?.toFixed(4) ?? "-";
        document.getElementById("z3Display").textContent = p.z3?.toFixed(4) ?? "-";
        document.getElementById("z4Display").textContent = p.z4?.toFixed(4) ?? "-";
        
        if (data.rb_surfaces) {
            render3DPlot("plot-rb-a1-a2", data.rb_surfaces.a1, data.rb_surfaces.a2, data.rb_surfaces.rb_a1_a2, "a1", "a2", "Rb");
            render3DPlot("plot-rb-gamma-b", data.rb_surfaces.gamma, data.rb_surfaces.b, data.rb_surfaces.rb_gamma_b, "γ", "b", "Rb");
            render3DPlot("plot-rb-p-k", data.rb_surfaces.p, data.rb_surfaces.k, data.rb_surfaces.rb_p_k, "p", "k", "Rb");
            render3DPlot("plot-rb-g-k", data.rb_surfaces.g, data.rb_surfaces.k, data.rb_surfaces.rb_g_k, "g", "k", "Rb");
        }
    })
    .catch(error => {
        console.error("Error en la petición:", error);
        // alert("Error al procesar la simulación.");
    });
}

let sim1Data = null;

function renderChart2D(data, modo) {
    const ctx = document.getElementById("chartTuberculosis").getContext("2d");

    const baseColors = {
        S: "#0000FF",    // blue
        E: "#FFA500",    // orange
        I: "#FF0000",    // red
        J: "#800080",    // purple
        T: "#008000",    // green
        R: "#808080"     // gray
    };

    // 💡 Convierte HEX a RGBA con opacidad
    const lighten = (hex, alpha = 0.6) => {
        const bigint = parseInt(hex.slice(1), 16);
        const r = (bigint >> 16) & 255;
        const g = (bigint >> 8) & 255;
        const b = bigint & 255;
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    };

    const variables = Object.keys(baseColors); // ["S", "E", "I", "J", "T", "R"]

    if (modo === 1) {
        sim1Data = data; // Guardamos datos de Sim 1
    }

    const combinedData = {
        labels: data.time,
        datasets: []
    };

    // Línea 1: Simulación 1
    if (sim1Data) {
        variables.forEach(key => {
            combinedData.datasets.push({
                label: `${key} (Sim 1)`,
                data: sim1Data[key],
                borderColor: baseColors[key],
                fill: false,
                tension: 0.2
            });
        });
    }

    // Línea 2: Simulación 2
    if (modo === 2) {
        variables.forEach(key => {
            combinedData.datasets.push({
                label: `${key} (Sim 2)`,
                data: data[key],
                borderColor: lighten(baseColors[key], 0.6), // mismo color pero más claro
                fill: false,
                borderDash: [5, 5], // opcional: línea punteada
                tension: 0.2
            });
        });
    }

    // Destruir y crear nuevo gráfico
    if (window.chartInstance) window.chartInstance.destroy();

    window.chartInstance = new Chart(ctx, {
        type: "line",
        data: combinedData,
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: {
                    display: true,
                    text: "Evolución de poblaciones"
                }
            },
            scales: {
                x: {
                    title: { display: true, text: "Tiempo (días)" }
                },
                y: {
                    title: { display: true, text: "Cantidad de personas" },
                    beginAtZero: true
                }
            }
        }
    });
}



document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM listo, anclando listeners");

  // Botones
  document.getElementById("sim1Btn")
          .addEventListener("click", () => runSimulation(1));
  document.getElementById("sim2Btn")
          .addEventListener("click", () => runSimulation(2));


  // Slider de días
  const slider = document.getElementById('dayRange'),
        display = document.getElementById('dayValue');

  display.textContent = slider.value;

  slider.addEventListener('input', () => {
      display.textContent = slider.value;

      // Ejecuta ambas simulaciones automáticamente
      runSimulation(1);
      runSimulation(2);
  });
});
