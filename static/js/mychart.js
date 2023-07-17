// ▼ トップページ ▼ //
const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      // labels: [
      //   '食材費',
      //   '交際費',
      //   '日用品',
      //   '固定費',
      //   'その他'
      // ],
      datasets: [{
        // label: 'My First Dataset',
        data: [30, 15, 15, 25, 15],
        backgroundColor: [
          'rgb(231, 129, 82)',
          'rgb(254, 202, 118)',
          'rgb(103, 181, 189)',
          'rgb(223, 81, 68)',
          'rgb(248, 235, 200)'
        ],
        hoverOffset: 4
      }]
    }
  });
// ▲ トップページ ▲ //
