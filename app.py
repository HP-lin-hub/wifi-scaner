from flask import Flask, render_template, jsonify, request
import subprocess
import json
import re

app = Flask(__name__)

# Импортируем наш сканер
from scanner import WiFiScanner

# Создаем экземпляр сканера
wifi_scanner = WiFiScanner()


def get_available_interfaces():
    """Получение списка всех доступных WiFi интерфейсов"""
    try:
        # Используем iw для получения информации об интерфейсах
        result = subprocess.run(["iw", "dev"],
                                capture_output=True, text=True, timeout=10)

        interfaces = []
        current_iface = None

        # Парсим вывод iw dev
        for line in result.stdout.split('\n'):
            line = line.strip()

            if line.startswith("Interface"):
                if current_iface:
                    interfaces.append(current_iface)
                iface_name = line.split()[1]
                current_iface = {"name": iface_name, "type": "unknown", "supported": True}

            elif "type" in line and current_iface:
                current_iface["type"] = line.split()[1]

        # Добавляем последний интерфейс
        if current_iface:
            interfaces.append(current_iface)

        # Если интерфейсы не найдены, пробуем другие методы
        if not interfaces:
            # Пробуем ip link
            try:
                ip_result = subprocess.run(["ip", "link", "show"],
                                           capture_output=True, text=True, timeout=10)
                for line in ip_result.stdout.split('\n'):
                    if "wl" in line and "state" in line:
                        iface_name = line.split(':')[1].strip()
                        interfaces.append({
                            "name": iface_name,
                            "type": "managed",
                            "supported": True
                        })
            except:
                pass

        return interfaces if interfaces else [
            {"name": "wlan0", "type": "managed", "supported": True},
            {"name": "wlp0s20f0u2", "type": "managed", "supported": True}
        ]

    except Exception as e:
        print(f"Error getting interfaces: {e}")
        return [{"name": "wlan0", "type": "managed", "supported": True}]


@app.route('/')
def index():
    """Главная страница"""
    interfaces = get_available_interfaces()
    return render_template('index.html', interfaces=interfaces)


@app.route('/scan', methods=['POST'])
def scan():
    """Endpoint для сканирования сетей"""
    try:
        data = request.get_json()
        selected_bands = data.get("bands", ["2.4 ГГц"])
        interface = data.get("interface", "")

        print(f"Scan request: interface={interface}, bands={selected_bands}")

        # Если интерфейс не выбран, используем первый доступный
        if not interface:
            interfaces = get_available_interfaces()
            if interfaces:
                interface = interfaces[0]["name"]
            else:
                return jsonify({"error": "No WiFi interfaces found"})

        # Проверяем доступность интерфейса
        interfaces = get_available_interfaces()
        interface_names = [iface["name"] for iface in interfaces]

        if interface not in interface_names:
            return jsonify({"error": f"Интерфейс {interface} недоступен. Доступные: {', '.join(interface_names)}"})

        # Устанавливаем выбранный интерфейс и диапазоны
        wifi_scanner.interface = interface
        wifi_scanner.set_bands(selected_bands)

        # Выполняем сканирование
        scan_result = wifi_scanner.scan()

        return jsonify(scan_result)

    except Exception as e:
        return jsonify({"error": f"Ошибка сканирования: {str(e)}"})


@app.route('/interfaces')
def get_interfaces():
    """Получить доступные интерфейсы"""
    interfaces = get_available_interfaces()
    return jsonify({"interfaces": interfaces})


@app.route('/vendor-db-status')
def vendor_db_status():
    """Проверка статуса базы производителей"""
    try:
        vendors_count = len(wifi_scanner.mac_vendors)

        # Проверяем несколько известных префиксов
        test_prefixes = {
            "a0:de:0f": "Huawei Technologies Co., Ltd",
            "d8:47": "TP-Link Corporation Limited",
            "28:ff:3e": "ZTE Corporation"
        }

        test_results = {}
        for prefix, expected_vendor in test_prefixes.items():
            actual_vendor = wifi_scanner.get_vendor_by_mac(prefix + ":00:00:00")
            test_results[prefix] = {
                "expected": expected_vendor,
                "actual": actual_vendor,
                "match": actual_vendor == expected_vendor
            }

        return jsonify({
            "vendors_count": vendors_count,
            "test_results": test_results,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/diagnostics')
def diagnostics():
    """Диагностика системы"""
    try:
        # Проверяем доступность iw
        iw_result = subprocess.run(["iw", "--version"],
                                   capture_output=True, text=True)

        # Проверяем доступность интерфейсов
        interfaces = get_available_interfaces()

        # Проверяем права sudo
        sudo_result = subprocess.run(["sudo", "-n", "iw", "dev"],
                                     capture_output=True, text=True)

        return jsonify({
            "iw_available": iw_result.returncode == 0,
            "iw_version": iw_result.stdout.split('\n')[0] if iw_result.returncode == 0 else iw_result.stderr,
            "interfaces": interfaces,
            "has_sudo": sudo_result.returncode == 0,
            "sudo_error": sudo_result.stderr if sudo_result.returncode != 0 else "OK"
        })

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/test-security')
def test_security():
    """Тестирование определения безопасности"""
    test_blocks = [
        # Добавьте примеры из вашего дампа для тестирования
    ]

    results = []
    for block in test_blocks:
        security = wifi_scanner.enhanced_security_detection(block)
        results.append({"block": block[:100] + "...", "security": security})

    return jsonify({"results": results})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
