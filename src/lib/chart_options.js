const colorhash = function(s) {
  return '#' + (s.getHashCode()).toString(16).padStart(6, '0');
};
const chart_options = {
  type: 'line',
  data: [],
  options: {
    animation: {
      duration: 0,
    },
    tooltips: {
        callbacks: {
            label(item, data) {
                let c = data.datasets[item.datasetIndex].data[item.index]
                return c.name+":"+c.score
            }
        }
    },
    scales: {
      xAxes: [{
        type: 'time',
        display: true,
        ticks: {
          padding: 10
        }
      }],
      yAxes: [{
        ticks: {
          padding: 10,
        }
      }]
    }
  }
}
export {colorhash, chart_options}
