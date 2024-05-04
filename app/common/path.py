def convert_to_wsl_path(path):
    """ WindowsパスをWSLパスに変換する """
    path = path.replace("\\", "/")
    drive = path.split(":")[0].lower()
    return f"/mnt/{drive}{path.split(':')[1]}"

def convert_to_win_path(path):
    """ WSLパスをWindowsパスに変換する """
    drive = path.split("/")[2].upper()
    return "{}:{}".format(drive, "\\" + "\\".join(path.split("/")[3:]))