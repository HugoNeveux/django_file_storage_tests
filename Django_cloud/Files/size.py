def format_bytes(size):
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size >= 1024:
        size /= 1024
        n += 1
    return str(round(size, 2)) + power_labels[n]
