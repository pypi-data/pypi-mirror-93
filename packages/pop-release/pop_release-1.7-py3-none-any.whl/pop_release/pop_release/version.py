# Import python libs
import glob
import os


def set_doc(hub):
    """
    Set the version on the docs
    """
    ver = hub.OPT["pop_release"]["ver"]
    name = hub.pop_release.PATHNAME
    lines = []
    paths = [os.path.join("docs", "conf.py"), os.path.join("docs", "source", "conf.py")]
    path = None
    for check in paths:
        if os.path.isfile(check):
            path = check
    if not path:
        print("No docs set up for this project, use Sphinx to set up docs")
        return
    with open(path, "r") as rfh:
        for line in rfh.readlines():
            if line.startswith("ver"):
                lines.append(f'version = "{ver}"\n')
                continue
            elif line.startswith("release"):
                lines.append(f'release = "{ver}"\n')
                continue
            else:
                lines.append(line)
    with open(path, "w+") as wfh:
        wfh.writelines(lines)


def set_ver(hub):
    """
    Set the version to the <project name>/version.py
    """
    ver = hub.OPT["pop_release"]["ver"]
    name = hub.pop_release.PATHNAME
    ver_str = f'# -*- coding: utf-8 -*-\nversion = "{ver}"\n'
    path = os.path.join(name, "version.py")

    if not os.path.exists(path):
        # try and find the path from a relative path
        paths = glob.glob(os.path.join("*", "version.py"))

        if paths:
            path = paths[0]

    if os.path.exists(path):
        with open(path, "w+") as wfh:
            wfh.write(ver_str)
