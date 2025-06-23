document.getElementById("startSim").addEventListener("click", function () {
    const params = {
        u: parseFloat(document.getElementById("u").value),
        n: parseFloat(document.getElementById("n").value),
        beta: parseFloat(document.getElementById("beta").value),
        c: parseFloat(document.getElementById("c").value),
        g: parseFloat(document.getElementById("g").value),
        h: parseFloat(document.getElementById("h").value),
        k: parseFloat(document.getElementById("k").value),
        r: parseFloat(document.getElementById("r").value),
        gamma: parseFloat(document.getElementById("gamma").value),
        p: parseFloat(document.getElementById("p").value),
        d1: parseFloat(document.getElementById("d1").value),
        d2: parseFloat(document.getElementById("d2").value)
    };

    fetch("/run_simulation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error en la simulación: " + data.error);
            return;
        }

        renderChart2D(data);

        if (data.rb_surfaces) {
            render3DPlot("plot-rb-a1-a2", data.rb_surfaces.a1, data.rb_surfaces.a2, data.rb_surfaces.rb_a1_a2, "a1", "a2", "Rb");
            render3DPlot("plot-rb-gamma-b", data.rb_surfaces.gamma, data.rb_surfaces.b, data.rb_surfaces.rb_gamma_b, "γ", "β", "Rb");
            render3DPlot("plot-rb-p-k", data.rb_surfaces.p, data.rb_surfaces.k, data.rb_surfaces.rb_p_k, "p", "k", "Rb");
            render3DPlot("plot-rb-g-k", data.rb_surfaces.g, data.rb_surfaces.k, data.rb_surfaces.rb_g_k, "g", "k", "Rb");
        }
    })
    .catch(error => {
        console.error("Error en la petición:", error);
        alert("Error al procesar la simulación.");
    });
});

function renderChart2D(data) {
    const ctx = document.getElementById("chartTuberculosis").getContext("2d");
    if (window.chartInstance) window.chartInstance.destroy();

    window.chartInstance = new Chart(ctx, {
        type: "line",
        data: {
            labels: data.time,
            datasets: [
                { label: "S", data: data.S, borderColor: "blue", fill: false },
                { label: "E", data: data.E, borderColor: "orange", fill: false },
                { label: "I", data: data.I, borderColor: "red", fill: false },
                { label: "J", data: data.J, borderColor: "purple", fill: false },
                { label: "L", data: data.L, borderColor: "green", fill: false },
                { label: "R", data: data.R, borderColor: "gray", fill: false }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: "Evolución de poblaciones" }
            }
        }
    });
}

function render3DPlot(containerId, x, y, z, xlabel, ylabel, zlabel) {
    const surface = {
        type: 'surface',
        x: x,
        y: y,
        z: z,
        colorscale: 'Viridis'
    };

    const layout = {
        title: `Gráfico 3D de ${zlabel} vs ${xlabel} y ${ylabel}`,
        scene: {
            xaxis: { title: xlabel },
            yaxis: { title: ylabel },
            zaxis: { title: zlabel }
        },
        margin: { l: 0, r: 0, b: 0, t: 40 }
    };

    Plotly.newPlot(containerId, [surface], layout);
}
