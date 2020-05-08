import os

def format_bytes(size):
    """ A function to format a bytes object into human readable
        size (adding an extension : B, KB, MB, GB, TB)"""
    n = 0
    power_labels = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size >= 1024:
        size /= 1024
        n += 1
    return str(round(size, 2)) + power_labels[n]

def recursive_file_list(dir):
    """ A function to recursivly scan folder for files, which
        return a list of relative paths to these files"""
    filelist = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filelist.append(os.path.join(root, file))

    return filelist
