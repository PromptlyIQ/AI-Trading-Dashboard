<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Trading Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .chart-container { width: 80%; margin: 20px auto; }
        table { width: 80%; margin: 20px auto; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid black; }
        th { background-color: #f4f4f4; }
        .alert-box { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>AI Trading Dashboard</h1>
    <div class="chart-container">
        <canvas id="tradeChart"></canvas>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Stock</th>
                <th>Current Price</th>
                <th>Predicted Move</th>
                <th>TradingView Analysis</th>
                <th>Real-Time Alerts</th>
            </tr>
        </thead>
        <tbody id="tradeTable">
        </tbody>
    </table>
    
    <div id="realTimeAlerts" class="alert-box"></div>
    
    <script>
        function fetchLiveData() {
            $.getJSON('/live-data', function(data) {
                let tableHtml = '';
                let labels = [];
                let prices = [];
                let alerts = '';
                
                Object.keys(data).forEach(stock => {
                    let item = data[stock];
                    let alertMessage = '';
                    
                    if (item.predicted_move > 0.02) {
                        alertMessage = `🚀 Breakout Alert: ${stock} expected to rise!`;
                    } else if (item.predicted_move < -0.02) {
                        alertMessage = `⚠️ Reversal Alert: ${stock} showing sell signals!`;
                    }
                    
                    tableHtml += `<tr>
                        <td>${stock}</td>
                        <td>${item.current_price.toFixed(2)}</td>
                        <td>${(item.predicted_move * 100).toFixed(2)}%</td>
                        <td>${item.tradingview_analysis}</td>
                        <td>${alertMessage}</td>
                    </tr>`;
                    labels.push(stock);
                    prices.push(item.current_price);
                    
                    if (alertMessage) {
                        alerts += `<p>${alertMessage}</p>`;
                    }
                });
                
                $('#tradeTable').html(tableHtml);
                $('#realTimeAlerts').html(alerts);
                
                let ctx = document.getElementById('tradeChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Stock Prices',
                            data: prices,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)'
                        }]
                    }
                });
            });
        }
        
        setInterval(fetchLiveData, 5000); // Refresh data every 5 seconds
        fetchLiveData();
    </script>
</body>
</html>
