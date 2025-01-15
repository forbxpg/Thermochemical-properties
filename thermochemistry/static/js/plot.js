function calculateHeat(a, b, c, d, e, f, g, T) {
    let temp = T * 10 ** (-4);
    return b + 2 * c * temp ** (-2) + 2 * e * temp + 6 * f * temp ** 2 + 12 * g * temp ** 3;
}

function calculateEntropy(a, b, c, d, e, f, g, T) {
    let temp = T * 10 ** (-4);
    return a + b * Math.log(temp) + b - c * temp ** (-2) + 2 * e * temp + 3 * f * temp ** 2 + 4 * g * temp ** 3;
}

function calculateEnthalpy(a, b, c, d, e, f, g, T) {
    let temp = T * 10 ** (-4);
    return (b * temp - 2 * c * temp ** (-1) - d + e * temp ** 2 + 2 * f * temp ** 3 + 3 * g * temp ** 4) * 10;
}

function plotGraph(a, b, c, d, e, f, g, temperatures) {
    var cp_values = temperatures.map(T => calculateHeat(a, b, c, d, e, f, g, T));
    var h_values = temperatures.map(T => calculateEnthalpy(a, b, c, d, e, f, g, T));
    var s_values = temperatures.map(T => calculateEntropy(a, b, c, d, e, f, g, T));

    var trace1 = { x: temperatures, y: cp_values, type: 'scatter', name: 'Cp(T)' };
    var trace2 = { x: temperatures, y: h_values, type: 'scatter', name: 'H(T)' };
    var trace3 = { x: temperatures, y: s_values, type: 'scatter', name: 'S(T)' };

    var data = [trace1, trace2, trace3];
    var layout = {
        title: 'Свойства при различных температурах',
        xaxis: { title: 'Температура (K)' },
        yaxis: { title: 'Значение' }
    };

    Plotly.newPlot('graph', data, layout);
}
