<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Scanner Pro</title>
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #64748b;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --dark: #1e293b;
            --light: #f8fafc;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.98);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            position: relative;
        }

        .header h1 {
            color: var(--dark);
            margin: 0;
            font-size: 2.5em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            position: relative;
            padding-left: 50px;
            display: inline-block;
        }

        /* Стили для SVG-иконки WiFi */
        .wifi-icon {
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 40px;
            height: 40px;
            z-index: 2;
            fill: #667eea;
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
        }

        .interface-selection {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        }

        .band-selection {
            background: linear-gradient(135deg, #c2e9fb 0%, #a1c4fd 100%);
        }

        .scan-results {
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        }

        .btn {
            background: linear-gradient(135deg, var(--primary) 0%, #4f46e5 100%);
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 5px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
        }

        .btn:disabled {
            background: var(--secondary);
            cursor: not-allowed;
            transform: none;
        }

        .interface-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }

        .interface-btn {
            background: var(--light);
            border: 2px solid var(--primary);
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .interface-btn:hover {
            background: var(--primary);
            color: white;
        }

        .interface-btn.active {
            background: var(--primary);
            color: white;
        }

        .band-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }

        .band-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            transition: all 0.3s ease;
        }

        .band-item:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        .band-item input[type="checkbox"] {
            margin-right: 10px;
            transform: scale(1.2);
        }

        .network-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }

        .network-table th,
        .network-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        .network-table th {
            background: var(--primary);
            color: white;
            font-weight: 600;
        }

        .network-table tr:hover {
            background: #f1f5f9;
        }

        .signal-bar {
            display: inline-block;
            width: 100px;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin-right: 10px;
        }

        .signal-fill {
            height: 100%;
            background: linear-gradient(90deg, #ef4444, #f59e0b, #10b981);
            border-radius: 4px;
        }

        .loading {
            text-align: center;
            padding: 30px;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #e2e8f0;
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error-message {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            color: var(--danger);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border: 1px solid #fecaca;
        }

        .success-message {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            color: #065f46;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
            border: 1px solid #a7f3d0;
        }

        .vendor-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin: 2px;
        }

        .vendor-huawei { background: #ff0000; color: white; }
        .vendor-tp-link { background: #4a86e8; color: white; }
        .vendor-zte { background: #009900; color: white; }
        .vendor-realtek { background: #663399; color: white; }
        .vendor-70mai { background: #ff6600; color: white; }
        .vendor-cisco { background: #049fd9; color: white; }
        .vendor-dell { background: #0076ce; color: white; }
        .vendor-intel { background: #0071c5; color: white; }
        .vendor-apple { background: #000; color: white; }
        .vendor-hp { background: #0096d6; color: white; }
        .vendor-sony { background: #003791; color: white; }
        .vendor-other { background: var(--secondary); color: white; }

        @media (max-width: 768px) {
            .band-grid {
                grid-template-columns: 1fr;
            }

            .container {
                padding: 15px;
                margin: 10px;
            }

            .header h1 {
                font-size: 2em;
                padding-left: 40px;
            }

            .wifi-icon {
                width: 32px;
                height: 32px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                <svg class="wifi-icon" viewBox="0 0 24 24">
                    <path d="M12 21.7c-1.5 0-2.7-1.2-2.7-2.7s1.2-2.7 2.7-2.7 2.7 1.2 2.7 2.7-1.2 2.7-2.7 2.7zm0-16.7c-3.7 0-6.7 3-6.7 6.7 0 1.2 1.2 2.3 2.7 2.3s2.7-1 2.7-2.3c0-1.8 1.4-3.2 3.3-3.2s3.3 1.4 3.3 3.2c0 1.3 1.2 2.3 2.7 2.3s2.7-1 2.7-2.3c0-3.7-3-6.7-6.7-6.7zm0-5c-6.5 0-11.7 5.2-11.7 11.7 0 3.1 2.6 5.7 5.7 5.7s5.7-2.6 5.7-5.7c0-3.3-2.7-6-6-6s-6 2.7-6 6c0 1.7 1.3 3 3 3s3-1.3 3-3c0-1.1.9-2 2-2s2 .9 2 2c0 1.7 1.3 3 3 3s3-1.3 3-3c0-3.3-2.7-6-6-6zm10 11.7c0 1.7 1.3 3 3 3s3-1.3 3-3c0-6.5-5.2-11.7-11.7-11.7-1.7 0-3.3.4-4.8 1l1.7 1.7c1-.3 2-.5 3.1-.5 5.4 0 9.7 4.3 9.7 9.7z"/>
                </svg>
                WiFi Scanner Pro
            </h1>
            <p>Мощный сканер WiFi сетей для Ubuntu с поддержкой всех диапазонов</p>
        </div>

        <!-- Карточка выбора интерфейса -->
        <div class="card interface-selection">
            <h2>📡 Выберите WiFi интерфейс:</h2>
            <p>Обнаруженные интерфейсы:</p>
            <div class="interface-list" id="interface-list">
                <!-- Интерфейсы будут добавлены через JavaScript -->
            </div>
            <button class="btn" onclick="refreshInterfaces()">
                🔄 Обновить интерфейсы
            </button>
        </div>

        <!-- Карточка выбора диапазонов -->
        <div class="card band-selection">
            <h2>🎯 Выберите диапазоны для сканирования:</h2>
            <div class="band-grid" id="bands-container">
                <div class="band-item">
                    <label><input type="checkbox" name="band" value="2.4 ГГц" checked> 2.4 ГГц</label>
                    <div class="band-info">2401-2483 МГц</div>
                </div>
                <div class="band-item">
                    <label><input type="checkbox" name="band" value="U-NII-1 (5150–5250 МГц)"> U-NII-1 (5150–5250 МГц)</label>
                    <div class="band-info">5150-5250 МГц</div>
                </div>
                <div class="band-item">
                    <label><input type="checkbox" name="band" value="U-NII-2 (5250–5350 МГц)"> U-NII-2 (5250–5350 МГц)</label>
                    <div class="band-info">5250-5350 МГц</div>
                </div>
                <div class="band-item">
                    <label><input type="checkbox" name="band" value="U-NII-2 Extended (5470–5725 МГц)"> U-NII-2 Extended (5470–5725 МГц)</label>
                    <div class="band-info">5470-5725 МГц</div>
                </div>
                <div class="band-item">
                    <label><input type="checkbox" name="band" value="U-NII-3 (5725–5850 МГц)"> U-NII-3 (5725–5850 МГц)</label>
                    <div class="band-info">5725-5850 МГц</div>
                </div>
                <div class="band-item">
                    <label><input type="checkbox" name="band" value="6 ГГц (Wi-Fi 6E)"> 6 ГГц (Wi-Fi 6E)</label>
                    <div class="band-info">5925-7125 МГц</div>
                </div>
            </div>
        </div>

        <!-- Кнопка сканирования -->
        <div style="text-align: center; margin: 20px 0;">
            <button class="btn" id="scan-button" onclick="scanNetworks()">
                🚀 Сканировать сети
            </button>
            <button class="btn" onclick="runDiagnostics()">
                🔧 Диагностика
            </button>
        </div>

        <!-- Индикатор загрузки -->
        <div class="card loading" id="loading" style="display: none;">
            <div class="spinner"></div>
            <p>Сканирование... Это может занять несколько минут</p>
            <p>Проверяем диапазоны: <span id="scanning-bands"></span></p>
        </div>

        <!-- Сообщения об ошибках и успехах -->
        <div class="error-message" id="error-message" style="display: none;"></div>
        <div class="success-message" id="success-message" style="display: none;"></div>

        <!-- Результаты сканирования -->
        <div class="card scan-results">
            <h2>📊 Обнаруженные сети:</h2>
            <div id="networks"></div>
        </div>
    </div>

    <script>
        let currentInterface = "";
        let availableInterfaces = [];

        // Загрузка данных при старте
        document.addEventListener('DOMContentLoaded', function() {
            loadInterfaces();
        });

        // Загрузка интерфейсов
        async function loadInterfaces() {
            try {
                const response = await fetch('/interfaces');
                const data = await response.json();
                availableInterfaces = data.interfaces;
                renderInterfaceList();
            } catch (error) {
                console.error('Ошибка загрузки интерфейсов:', error);
                availableInterfaces = [
                    {name: "wlan0", type: "managed", supported: true},
                    {name: "wlp0s20f0u2", type: "managed", supported: true}
                ];
                renderInterfaceList();
            }
        }

        function renderInterfaceList() {
            const container = document.getElementById('interface-list');
            container.innerHTML = '';

            availableInterfaces.forEach(iface => {
                const btn = document.createElement('button');
                btn.className = 'interface-btn';
                btn.textContent = `${iface.name} (${iface.type})`;
                btn.onclick = () => selectInterface(iface.name);

                if (iface.name === currentInterface) {
                    btn.classList.add('active');
                }

                container.appendChild(btn);
            });

            // Автовыбор первого интерфейса
            if (availableInterfaces.length > 0 && !currentInterface) {
                selectInterface(availableInterfaces[0].name);
            }
        }

        function selectInterface(interface) {
            currentInterface = interface;
            renderInterfaceList();
            showSuccess(`Выбран интерфейс: ${interface}`);
        }

        async function scanNetworks() {
            if (!currentInterface) {
                showError('Пожалуйста, выберите интерфейс');
                return;
            }

            const selectedBands = getSelectedBands();
            if (selectedBands.length === 0) {
                showError('Пожалуйста, выберите хотя бы один диапазон');
                return;
            }

            // Показываем индикатор загрузки
            document.getElementById('loading').style.display = 'block';
            document.getElementById('scan-button').disabled = true;
            document.getElementById('error-message').style.display = 'none';
            document.getElementById('success-message').style.display = 'none';

            // Показываем какие диапазоны сканируются
            document.getElementById('scanning-bands').textContent =
                selectedBands.join(', ');

            try {
                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        bands: selectedBands,
                        interface: currentInterface
                    })
                });

                const data = await response.json();

                if (data.error) {
                    showError(data.error);
                } else {
                    displayNetworks(data.networks || []);
                    showSuccess(`Найдено ${data.networks.length} сетей`);
                }
            } catch (error) {
                showError('Ошибка при сканировании: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('scan-button').disabled = false;
            }
        }

        function getSelectedBands() {
            const selectedBands = [];
            document.querySelectorAll('input[name="band"]:checked').forEach(checkbox => {
                selectedBands.push(checkbox.value);
            });
            return selectedBands;
        }

        function displayNetworks(networks) {
            const networksDiv = document.getElementById('networks');

            if (networks.length === 0) {
                networksDiv.innerHTML = '<p>Сети не найдены</p>';
                return;
            }

            let table = `
            <table class="network-table">
                <tr>
                    <th>SSID</th>
                    <th>BSSID</th>
                    <th>Частота (МГц)</th>
                    <th>Сигнал (dBm)</th>
                    <th>Безопасность</th>
                    <th>Производитель</th>
                </tr>
            `;

            networks.forEach(network => {
                const signalStrength = Math.min(100, Math.max(0, parseInt(network.signal || 0) + 100));
                const vendorName = network.vendor || 'Unknown';
                // Создаем класс CSS на основе имени производителя
                const vendorClass = vendorName.toLowerCase().replace(/[^a-z0-9]+/g, '-');

                table += `
                <tr>
                    <td>${network.ssid || '<скрытая сеть>'}</td>
                    <td>${network.bssid}</td>
                    <td>${network.frequency}</td>
                    <td>
                        <div class="signal-bar">
                            <div class="signal-fill" style="width: ${signalStrength}%"></div>
                        </div>
                        ${network.signal}
                    </td>
                    <td>${network.security || 'Открытая'}</td>
                    <td><span class="vendor-badge vendor-${vendorClass}">${vendorName}</span></td>
                </tr>
                `;
            });

            table += '</table>';
            networksDiv.innerHTML = table;
        }

        async function runDiagnostics() {
            try {
                const response = await fetch('/diagnostics');
                const data = await response.json();

                let diagnosticInfo = `
                    <strong>iw доступен:</strong> ${data.iw_available ? 'Да' : 'Нет'}<br>
                    <strong>Версия iw:</strong> ${data.iw_version || 'Не доступна'}<br>
                    <strong>Права sudo:</strong> ${data.has_sudo ? 'Есть' : 'Нет'}<br>
                    <strong>Ошибка sudo:</strong> ${data.sudo_error || 'Нет'}<br>
                    <strong>Доступные интерфейсы:</strong><br>
                `;

                data.interfaces.forEach(iface => {
                    diagnosticInfo += `- ${iface.name} (${iface.type})<br>`;
                });

                showSuccess(diagnosticInfo);
            } catch (error) {
                showError('Ошибка диагностики: ' + error.message);
            }
        }

        async function refreshInterfaces() {
            await loadInterfaces();
            showSuccess('Интерфейсы обновлены');
        }

        function showError(message) {
            const errorDiv = document.getElementById('error-message');
            errorDiv.innerHTML = message;
            errorDiv.style.display = 'block';
            document.getElementById('success-message').style.display = 'none';
        }

        function showSuccess(message) {
            const successDiv = document.getElementById('success-message');
            successDiv.innerHTML = message;
            successDiv.style.display = 'block';
            document.getElementById('error-message').style.display = 'none';
        }
    </script>
</body>
</html>
