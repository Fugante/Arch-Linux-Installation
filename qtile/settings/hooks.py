import os
import subprocess

from libqtile import hook


@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser('~/.config/qtile/settings/autostart.sh')
    subprocess.call([script], shell=True)