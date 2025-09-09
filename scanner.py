import subprocess
import re
import json
import os
from typing import List, Dict

# Диапазоны WiFi и соответствующие частоты (в МГц)
BAND_FREQUENCIES = {
    "2.4 ГГц": [2412, 2417, 2422, 2427, 2432, 2437, 2442, 2447, 2452, 2457, 2462, 2467, 2472, 2484],
    "U-NII-1 (5150–5250 МГц)": [5180, 5200, 5220, 5240],
    "U-NII-2 (5250–5350 МГц)": [5260, 5280, 5300, 5320],
    "U-NII-2 Extended (5470–5725 МГц)": [5500, 5520, 5540, 5560, 5580, 5600, 5620, 5640, 5660, 5680, 5700, 5720],
    "U-NII-3 (5725–5850 МГц)": [5745, 5765, 5785, 5805, 5825],
    "6 ГГц (Wi-Fi 6E)": [5955, 5975, 5995, 6015, 6035, 6055, 6075, 6095, 6115, 6135, 6155, 6175, 6195, 6215, 6235, 6255,
                         6275, 6295, 6315, 6335]
}


class WiFiScanner:
    def __init__(self, interface: str = ""):
        self.interface = interface
        self.selected_bands = ["2.4 ГГц"]
        self.mac_vendors = self.load_mac_vendors()

    def load_mac_vendors(self):
        """Загрузка базы производителей из JSON файла в новом формате"""
        try:
            vendors_file = os.path.join(os.path.dirname(__file__), 'mac_vendors.json')
            with open(vendors_file, 'r', encoding='utf-8') as f:
                vendors_data = json.load(f)

            # Преобразуем в словарь для быстрого поиска
            vendors_dict = {}
            for item in vendors_data:
                if 'macPrefix' in item and 'vendorName' in item:
                    # Нормализуем MAC-префикс (убираем тире, если есть)
                    mac_prefix = item['macPrefix'].replace('-', ':').lower()
                    vendors_dict[mac_prefix] = item['vendorName']

            print(f"Загружено {len(vendors_dict)} производителей из базы данных")
            return vendors_dict

        except FileNotFoundError:
            print("Файл базы производителей mac_vendors.json не найден")
            return {}
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения файла базы производителей: {e}")
            return {}
        except Exception as e:
            print(f"Неожиданная ошибка при загрузке базы производителей: {e}")
            return {}

    def get_vendor_by_mac(self, mac_address):
        """Определение производителя по MAC-адресу с использованием новой базы"""
        if not self.mac_vendors:
            return "Unknown"

        # Нормализуем MAC-адрес
        mac = mac_address.lower().replace('-', ':')

        # Пробуем найти производителя по префиксам разной длины
        for prefix_length in [8, 5, 2]:  # 6, 3, 1 байт соответственно (a0:de:0f, a0:de, a0)
            prefix = mac[:prefix_length]
            if prefix in self.mac_vendors:
                return self.mac_vendors[prefix]

        return "Unknown"

    def set_bands(self, bands: List[str]):
        """Установить выбранные диапазоны"""
        self.selected_bands = bands

    def check_interface_exists(self) -> bool:
        """Проверить существование интерфейса"""
        if not self.interface:
            return False

        try:
            result = subprocess.run(["ip", "link", "show", self.interface],
                                    capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def check_rfkill_unblock(self):
        """Разблокировать WiFi через rfkill"""
        try:
            subprocess.run(["sudo", "rfkill", "unblock", "wifi"],
                           capture_output=True)
            subprocess.run(["sudo", "rfkill", "unblock", "all"],
                           stderr=subprocess.DEVNULL)
            return True
        except:
            return False

    def get_supported_bands(self) -> List[str]:
        """Получить список поддерживаемых диапазонов"""
        try:
            # Проверяем поддержку 6 ГГц
            result = subprocess.run(["iw", "phy", "phy0", "info"],
                                    capture_output=True, text=True)
            output = result.stdout.lower()

            supported_bands = ["2.4 ГГц"]

            if any(freq in output for freq in ["5150", "5180", "5200"]):
                supported_bands.extend(["U-NII-1 (5150–5250 МГц)", "U-NII-2 (5250–5350 МГц)"])

            if any(freq in output for freq in ["5470", "5500", "5720"]):
                supported_bands.append("U-NII-2 Extended (5470–5725 МГц)")

            if any(freq in output for freq in ["5725", "5745", "5825"]):
                supported_bands.append("U-NII-3 (5725–5850 МГц)")

            # Проверяем поддержку 6 ГГц (Wi-Fi 6E)
            if any(freq in output for freq in ["5955", "5975", "6115"]):
                supported_bands.append("6 ГГц (Wi-Fi 6E)")

            return supported_bands

        except Exception as e:
            print(f"Error checking supported bands: {e}")
            return list(BAND_FREQUENCIES.keys())

    def generate_scan_command(self) -> List[str]:
        """Сгенерировать команду для сканирования выбранных диапазонов"""
        if not self.interface:
            raise ValueError("Интерфейс не выбран")

        if not self.check_interface_exists():
            raise ValueError(f"Интерфейс {self.interface} не существует")

        # Разблокируем WiFi
        self.check_rfkill_unblock()

        frequencies = []
        for band in self.selected_bands:
            if band in BAND_FREQUENCIES:
                frequencies.extend(BAND_FREQUENCIES[band])

        if not frequencies:
            raise ValueError("Не выбраны диапазоны для сканирования")

        # Формируем команду iw с частотами
        cmd = ["sudo", "iw", "dev", self.interface, "scan"]
        for freq in frequencies:
            cmd.extend(["freq", str(freq)])

        return cmd

    def scan(self) -> Dict:
        """Выполнить сканирование выбранных диапазонов"""
        try:
            cmd = self.generate_scan_command()
            print(f"Executing command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                # Пробуем разблокировать и повторить
                self.check_rfkill_unblock()
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode != 0:
                    error_msg = result.stderr if result.stderr else "Unknown error"
                    return {"error": f"Ошибка сканирования: {error_msg}"}

            return self.parse_output(result.stdout)

        except subprocess.TimeoutExpired:
            return {"error": "Таймаут сканирования"}
        except Exception as e:
            return {"error": f"Ошибка: {str(e)}"}

    def parse_output(self, output: str) -> Dict:
        """Парсинг вывода команды iw scan (поблочный)"""
        networks = []
        # Разделяем вывод на блоки по BSS
        blocks = re.split(r'\nBSS ', output)

        for block in blocks:
            if not block.strip():
                continue

            # Добавляем обратно "BSS " к каждому блоку, кроме первого
            if not block.startswith("BSS"):
                block = "BSS " + block

            current_ap = self.parse_block(block)
            if current_ap and current_ap.get("bssid"):
                # Фильтрация по выбранным диапазонам
                if self.is_in_selected_bands(current_ap.get("frequency", "")):
                    networks.append(current_ap)

        return {"networks": networks}

    def is_in_selected_bands(self, frequency_str: str) -> bool:
        """Проверить, принадлежит ли частота выбранным диапазонам"""
        if not frequency_str or not self.selected_bands:
            return True

        try:
            freq = int(float(frequency_str))
            for band in self.selected_bands:
                if band in BAND_FREQUENCIES and freq in BAND_FREQUENCIES[band]:
                    return True
            return False
        except (ValueError, TypeError):
            return True

    def parse_block(self, block: str) -> Dict:
        """Парсинг одного блока с информацией о сети"""
        lines = block.split('\n')
        current_ap = {
            "bssid": "",
            "ssid": "Hidden",
            "frequency": "",
            "signal": "",
            "security": "Open",
            "vendor": "Unknown"
        }

        # Регулярное выражение для извлечения MAC-адреса (учитываем скобки)
        mac_match = re.search(r'BSS ([0-9a-fA-F:]+)(?:\(| |$)', block)
        if mac_match:
            current_ap["bssid"] = mac_match.group(1)
            # Определяем производителя по MAC-адресу
            current_ap["vendor"] = self.get_vendor_by_mac(current_ap["bssid"])
        else:
            # Если не удалось извлечь MAC, пропускаем блок
            return None

        # Флаги для определения безопасности
        has_privacy = False
        has_rsn = False
        has_wpa = False
        has_wpa2 = False
        has_wpa3 = False
        has_wep = False

        # Детальная информация о безопасности
        security_details = {
            "group_cipher": "",
            "pairwise_ciphers": [],
            "auth_suites": [],
            "key_management": []
        }

        for line in lines:
            line = line.strip()

            # Парсим SSID
            if "SSID:" in line and not line.startswith("RSN") and not line.startswith("WPA"):
                ssid_match = re.search(r'SSID:\s*(.+)', line)
                if ssid_match:
                    current_ap["ssid"] = ssid_match.group(1).strip()

            # Парсим частоту
            elif "freq:" in line:
                freq_match = re.search(r'freq:\s*([\d.]+)', line)
                if freq_match:
                    current_ap["frequency"] = freq_match.group(1)

            # Парсим сигнал
            elif "signal:" in line:
                signal_match = re.search(r'signal:\s*([-\d.]+)', line)
                if signal_match:
                    current_ap["signal"] = signal_match.group(1)

            # Определяем безопасность - capability
            elif "capability:" in line:
                if "PRIVACY" in line:
                    has_privacy = True
                    has_wep = True  # PRIVACY обычно означает WEP

            # Анализ RSN (WPA2/WPA3)
            elif line.strip().startswith("RSN:"):
                has_rsn = True
                has_wpa2 = True

                # Детальный анализ RSN элементов
                if "CCMP" in line:
                    security_details["group_cipher"] = "CCMP"
                if "TKIP" in line:
                    security_details["group_cipher"] = "TKIP"
                if "PSK" in line:
                    security_details["auth_suites"].append("PSK")
                if "802.1X" in line or "EAP" in line:
                    security_details["auth_suites"].append("Enterprise")
                if "SAE" in line:
                    has_wpa3 = True
                    security_details["auth_suites"].append("SAE")

            # Анализ WPA (WPA1)
            elif line.strip().startswith("WPA:"):
                has_wpa = True
                if "CCMP" in line:
                    security_details["group_cipher"] = "CCMP"
                if "TKIP" in line:
                    security_details["group_cipher"] = "TKIP"
                if "PSK" in line:
                    security_details["auth_suites"].append("PSK")

            # Анализ информации о безопасности в других форматах
            elif "Authentication suites:" in line:
                if "PSK" in line:
                    security_details["auth_suites"].append("PSK")
                if "802.1X" in line or "EAP" in line:
                    security_details["auth_suites"].append("Enterprise")
                if "SAE" in line:
                    has_wpa3 = True
                    security_details["auth_suites"].append("SAE")

            # Определение OWE (Opportunistic Wireless Encryption)
            elif "OWE" in line:
                current_ap["security"] = "OWE"

        # Определяем тип безопасности на основе собранных данных
        if has_wpa3:
            current_ap["security"] = "WPA3"
        elif has_rsn and "SAE" in security_details["auth_suites"]:
            current_ap["security"] = "WPA3"
        elif has_rsn:
            current_ap["security"] = "WPA2"
        elif has_wpa:
            current_ap["security"] = "WPA"
        elif has_privacy and has_wep:
            current_ap["security"] = "WEP"
        else:
            current_ap["security"] = "Open"

        # Добавляем детальную информацию о безопасности
        current_ap["security_details"] = security_details

        return current_ap

    def enhanced_security_detection(self, block: str) -> str:
        """Улучшенное определение безопасности на основе полного анализа блока"""
        security = "Open"

        # Проверяем различные паттерны безопасности
        if "RSN:" in block and "PSK" in block:
            security = "WPA2-Personal"
        elif "RSN:" in block and "EAP" in block:
            security = "WPA2-Enterprise"
        elif "WPA:" in block and "PSK" in block:
            security = "WPA-Personal"
        elif "WPA:" in block and "EAP" in block:
            security = "WPA-Enterprise"
        elif "PRIVACY" in block:
            security = "WEP"
        elif "SAE" in block:
            security = "WPA3"
        elif "OWE" in block:
            security = "OWE"

        return security
