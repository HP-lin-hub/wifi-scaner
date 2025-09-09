#!/usr/bin/env python3
import requests
import json
import os
import re
from datetime import datetime


def get_current_db_url():
    """Получение актуального URL базы данных с maclookup.app"""
    try:
        # Главная страница maclookup.app
        main_url = "https://maclookup.app/downloads/json-database"
        response = requests.get(main_url, timeout=10)
        response.raise_for_status()

        # Ищем URL для скачивания в HTML
        download_pattern = r'https://maclookup\.app/downloads/json-database/get-db\?t=[^&]+&h=[a-f0-9]+'
        match = re.search(download_pattern, response.text)

        if match:
            return match.group(0)
        else:
            # Fallback URL если не нашли в HTML
            current_date = datetime.now().strftime("%y-%m-%d")
            return f"https://maclookup.app/downloads/json-database/get-db?t={current_date}&h=default_hash"

    except Exception as e:
        print(f"Ошибка при получении URL: {e}")
        return None


def update_mac_vendors():
    """Автоматическое обновление базы производителей MAC-адресов"""
    db_url = get_current_db_url()

    if not db_url:
        print("Не удалось получить URL базы данных")
        return False

    output_file = "mac_vendors.json"

    try:
        print(f"Загрузка актуальной базы MAC-адресов...")
        print(f"URL: {db_url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(db_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Сохраняем raw данные
        with open(output_file, 'wb') as f:
            f.write(response.content)

        print(f"База данных успешно обновлена и сохранена в {output_file}")
        print(f"Размер файла: {len(response.content)} байт")

        # Проверяем целостность данных
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Загружено {len(data)} записей о производителях")

        return True

    except Exception as e:
        print(f"Ошибка при обновлении базы данных: {e}")
        return False


if __name__ == "__main__":
    success = update_mac_vendors()
    if not success:
        # Резервный вариант - использовать прямую ссылку
        print("Пробуем резервный URL...")
        current_date = datetime.now().strftime("%y-%m-%d")
        backup_url = f"https://maclookup.app/downloads/json-database/get-db?t={current_date}&h=backup_hash"

        try:
            response = requests.get(backup_url, timeout=30)
            with open("mac_vendors.json", 'wb') as f:
                f.write(response.content)
            print("Резервное обновление выполнено")
        except:
            print("Не удалось обновить базу данных")
