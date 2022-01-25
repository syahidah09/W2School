const ctx = document.getElementById('myChart').getContext('2d');
const ctx2 = document.getElementById('myChart2');
const BARCHARTEXMPLE = document.getElementById('barChartExample');

const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [{% for ltr in ltr %} '{{ ltr.0 }}', {% endfor %}],
        datasets: [{
            label: 'Amount Spend',
            data: [{% for ltr in ltr %} '{{ ltr.1 }}', {% endfor %}],
            backgroundColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
            }],
        datalabels: {
            anchor: 'center',
                backgroundColor: null,
                    borderWidth: 0
        }
    },
    options: {
        responsive: true,
            animation: {
            animateScale: true,
                animateRotate: true
        },
        plugins: {
            datalabels: {
                backgroundColor: function(context) {
                    return context.dataset.backgroundColor;
                },
                borderColor: 'white',
                    borderRadius: 25,
                        borderWidth: 2,
                            color: 'white',
                                display: function(context) {
                                    var dataset = context.dataset;
                                    var count = dataset.data.length;
                                    var value = dataset.data[context.dataIndex];
                                    return value > count * 1.5;
                                },
                font: {
                    weight: 'bold'
                },
                padding: 6,
                    formatter: Math.round
            }
        },    
    },   
});
