const colorhash = function(s) {
  var hash = 0, i, chr;
  if (s.length === 0) return hash;
  for (i = 0; i < s.length; i++) {
    chr   = s.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return '#' + (hash % 0xfff).toString(16).padStart(3, '0');
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
