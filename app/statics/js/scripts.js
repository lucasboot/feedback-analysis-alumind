function renderCharts(feedbacks) {
    const sentiments = feedbacks.map(f => f.sentiment);
    const sentimentCounts = sentiments.reduce((acc, sentiment) => {
        acc[sentiment] = (acc[sentiment] || 0) + 1;
        return acc;
    }, {});

    const sentimentChart = new Chart(document.getElementById('sentimentChart'), {
        type: 'pie',
        data: {
            labels: Object.keys(sentimentCounts),
            datasets: [{
                data: Object.values(sentimentCounts),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
        }
    });

    const features = feedbacks.flatMap(f => f.requested_features.map(rf => rf.code));
    const featureCounts = features.reduce((acc, feature) => {
        acc[feature] = (acc[feature] || 0) + 1;
        return acc;
    }, {});

    const featuresChart = new Chart(document.getElementById('featuresChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(featureCounts),
            datasets: [{
                label: 'Requested Features',
                data: Object.values(featureCounts),
                backgroundColor: '#36A2EB'
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
