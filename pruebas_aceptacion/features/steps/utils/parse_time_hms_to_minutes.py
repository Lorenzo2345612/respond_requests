def parse_time_hms_to_minutes(s):
    # acepta formatos H:M:S o H:M
    parts = s.split(':')
    try:
        parts = [int(p) for p in parts]
    except Exception:
        return None
    if len(parts) == 3:
        h, m, sec = parts
    elif len(parts) == 2:
        h, m = parts
        sec = 0
    else:
        return None
    return h * 60 + m + round(sec / 60)