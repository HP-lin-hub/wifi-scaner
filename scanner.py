# scanner.py
import subprocess
import re

def freq_to_channel(freq):
    """Вычислить номер канала по частоте (MHz)."""
    try:
        f = int(float(freq))
    except Exception:
        return 0
    # 2.4 GHz channels
    if 2412 <= f <= 2484:
        return (f - 2407) // 5
    # 5 GHz
    if 5000 <= f <= 5900:
        return (f - 5000) // 5
    # 6 GHz (typical 5925..7125)
    if 5925 <= f <= 7125:
        return (f - 5950) // 5
    return 0

_RE_BSS = re.compile(
    r'(?m)^BSS\s+([0-9a-f:]{17})'                  # MAC
    r'(?:\([^\)]*\))?.*?'                          # optional "(on ...)" and rest of line
    r'(?=(?:\n^BSS\s+[0-9a-f:]{17})|\Z)',          # up to next BSS or EOF
    re.DOTALL | re.IGNORECASE
)

def _extract_pairwise(block):
    m = re.search(r'Pairwise ciphers:\s*(.*)', block, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # fallback: look for "Pairwise ciphers" inside RSN/WPA subsections (with bullets)
    m2 = re.search(r'Pairwise ciphers:\s*\n(?:\s*\*\s*)?([A-Za-z0-9 ,/]+)', block, re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return ""

def _extract_group_cipher(block):
    m = re.search(r'Group cipher:\s*(.*)', block, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""

def _extract_channel_from_block(block):
    m = re.search(r'DS Parameter set:\s*channel\s*(\d+)', block, re.IGNORECASE)
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    # sometimes: HT operation: * primary channel: N
    m2 = re.search(r'primary channel:\s*(\d+)', block, re.IGNORECASE)
    if m2:
        try:
            return int(m2.group(1))
        except:
            return None
    return None

def _extract_wps(block):
    """
    Возвращает строку: "✖" или "✔ : Version X" или "✔" если нет версии.
    Также учитывает состояние (Wi-Fi Protected Setup State: 2 — Configured).
    """
    m = re.search(r'WPS:\s*(?:\n(?:\s*[\*\w\-\:\(\)\.].*)+)?', block, re.IGNORECASE)
    if not m:
        return "✖"
    wps_block = m.group(0)
    ver = None
    state = None
    mv = re.search(r'\bVersion[:\s]*([\d\.]+)', wps_block, re.IGNORECASE)
    if mv:
        ver = mv.group(1).strip()
    ms = re.search(r'Wi-?Fi Protected Setup State[:\s]*([0-9]+)', wps_block, re.IGNORECASE)
    if ms:
        state = ms.group(1).strip()
    if ver and state:
        return f"✔ : Version {ver}" if state == "2" else f"✖ : Version {ver}"
    if ver:
        return f"✔ : Version {ver}"
    return "✔"

def parse_iw_scan(interface, freqs=[]):
    """
    interface - имя интерфейса (wlp..., wlan...)
    freqs - список строк: "2.4", "5", "6" — если пустой, возвращает все сети.
    Возвращает список словарей с полями:
    ssid, mac, channel, freq, signal, security, cipher, wps
    """
    networks = []
    try:
        res = subprocess.run(["iw", "dev", interface, "scan"],
                             capture_output=True, text=True, timeout=8)
        out = res.stdout
    except Exception as e:
        # Не падаем — возвращаем пустой список и печатаем ошибку (чтобы видно было в логах)
        print(f"[scanner] iw scan failed: {e}")
        return networks

    # Найдём все BSS-блоки при помощи регулярки (надёжнее, чем простое split)
    for m in _RE_BSS.finditer(out):
        mac = m.group(1).lower()
        block = m.group(0)

        # убираем возможные "(on ...)" в mac (на всякий случай)
        mac = mac.replace("(on", "").replace(")", "").strip()

        # Получаем SSID (может отсутствовать — скрытая сеть)
        ssid_m = re.search(r'^\s*SSID:\s*(.*)$', block, re.MULTILINE)
        ssid = ssid_m.group(1).strip() if ssid_m else ""

        # freq
        freq = None
        fm = re.search(r'^\s*freq:\s*([\d\.]+)', block, re.MULTILINE)
        if fm:
            try:
                freq = int(float(fm.group(1)))
            except:
                freq = None

        # signal
        sig = ""
        sm = re.search(r'^\s*signal:\s*([-0-9\.]+\s*dBm)', block, re.MULTILINE | re.IGNORECASE)
        if sm:
            sig = sm.group(1).strip()
        else:
            # иногда просто "signal: -65.00 dBm"
            sm2 = re.search(r'signal:\s*([-0-9\.]+)\s*dBm', block, re.IGNORECASE)
            if sm2:
                sig = f"{sm2.group(1).strip()} dBm"

        # channel — сначала пробуем извлечь явно, иначе по freq
        ch = _extract_channel_from_block(block)
        if not ch and freq:
            ch = freq_to_channel(freq)
        ch = ch or 0

        # security / cipher detection
        lower = block.lower()
        security = "Open"
        cipher = ""

        # WPA3: поиск SAE/OWE/DPP/WPA3
        if re.search(r'\bwpa3\b', lower) or re.search(r'\bsae\b', lower) or re.search(r'\bowe\b', lower) or re.search(r'\bdpp\b', lower):
            security = "WPA3"
            pairwise = _extract_pairwise(block)
            group = _extract_group_cipher(block)
            cipher = ", ".join(filter(None, [pairwise, group])) or "CCMP"

        # RSN -> WPA2
        elif 'rsn:' in lower or re.search(r'\brsn\b', lower):
            security = "WPA2"
            pairwise = _extract_pairwise(block)
            group = _extract_group_cipher(block)
            cipher = ", ".join(filter(None, [pairwise, group])) or "CCMP"

        # WPA (legacy) presence
        elif re.search(r'\bwpa:\b', block, re.IGNORECASE) or re.search(r'\bWPA:\s*\*', block):
            security = "WPA"
            pairwise = _extract_pairwise(block)
            group = _extract_group_cipher(block)
            cipher = ", ".join(filter(None, [pairwise, group])) or "TKIP"

        # WEP
        elif 'wep' in lower:
            security = "WEP"
            cipher = "WEP"

        # capability privacy fallback (если нет RSN/WPA/WEP, но есть Privacy в capability — считаем WPA2)
        else:
            cap_m = re.search(r'capability:\s*(.*)', lower)
            if cap_m and 'privacy' in cap_m.group(1):
                security = "WPA2"
                pairwise = _extract_pairwise(block)
                cipher = pairwise or "Unknown"

        # Если не нашлось cipher — попытаемся взять Pairwise/Group ещё раз
        if not cipher:
            pairwise = _extract_pairwise(block)
            group = _extract_group_cipher(block)
            cipher = ", ".join(filter(None, [pairwise, group])) or ""

        # WPS
        wps = _extract_wps(block)

        # Фильтрация по диапазонам (если указан freqs)
        if freqs and freq:
            band = ""
            if 2400 <= freq <= 2500: band = "2.4"
            elif 5000 <= freq <= 5900: band = "5"
            elif 5925 <= freq <= 7125: band = "6"
            if band not in freqs:
                continue

        # Добавляем запись (SSID может быть пустым — скрытые сети)
        networks.append({
            "ssid": ssid,
            "mac": mac,
            "channel": ch,
            "freq": freq or 0,
            "signal": sig,
            "security": security,
            "cipher": cipher,
            "wps": wps
        })

    return networks
