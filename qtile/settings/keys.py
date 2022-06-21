from typing import Callable, List, Tuple

from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy

from .groups import groups_data


KeyCmd = Tuple[List, str, Callable]

mod = 'mod4'
keys_cmds: List[KeyCmd] = [
    # ------------- Window Keys -------------
    # Switch window focus in current stack pane
    ([mod], 'h', lazy.layout.left()),
    ([mod], 'l', lazy.layout.right()),
    ([mod], 'k', lazy.layout.up()),
    ([mod], 'j', lazy.layout.down()),
    ([mod], 'space', lazy.layout.next()),
    # Move windows up, down, right or, left in current stack
    ([mod, 'shift'], 'k', lazy.layout.shuffle_up()),
    ([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
    ([mod, 'shift'], 'l', lazy.layout.shuffle_right()),
    ([mod, 'shift'], 'h', lazy.layout.shuffle_left()),
    # Flip window layout (MonadTall and MonadWide)
    ([mod, 'shift'], 'space', lazy.layout.flip()),
    # Toogle floating
    ([mod, 'shift'], 'f', lazy.window.toggle_floating()),
    # Grow windows
    ([mod, 'control'], 'k', lazy.layout.grow_up()),
    ([mod, 'control'], 'j', lazy.layout.grow_down()),
    ([mod, 'control'], 'l', lazy.layout.grow_right()),
    ([mod, 'control'], 'h', lazy.layout.grow_left()),
    # Change windows sizes (MonadTall and MonadWide)
    ([mod, 'control'], 'i', lazy.layout.grow()),
    ([mod, 'control'], 'm', lazy.layout.shrink()),
    # Toogle window maximum and minimum sizes
    ([mod, 'control'], 'o', lazy.layout.maximize()),
    # Reset window sizes
    ([mod], 'n', lazy.layout.normalize()),
    # Toggle between dirrerent layouts
    ([mod], 'Tab', lazy.next_layout()),
    # Kill focused window
    ([mod], 'w', lazy.window.kill()),

    # ------------- Qtile Keys -------------
    # Restart Qtile
    ([mod, 'control'], 'r', lazy.restart()),
    # Shutdown Qtile
    ([mod, 'control'], 'q', lazy.shutdown()),
    # Spawn a command using a prompt widget
    ([mod], 'r', lazy.spawncmd()),

    # ----------- Application Keys -----------
    # Launch terminal
    ([mod], 'Return', lazy.spawn('st')),
    # Launch file explorer
    ([mod], 'f', lazy.spawn('nautilus')),
    # Launch web browser
    ([mod], 'b', lazy.spawn('firefox')),
    # Print screen
    (
        [],
        'Print',
        lazy.spawn("scrot '%Y-%m-%d_%wx$h.png' -e 'mv $f ~/Pictures/'")
    ),
    (
        ['shift'],
        'Print',
        lazy.spawn("scrot -s '%Y-%m-%d_%wx$h.png' -e 'mv $f ~/Pictures/'")
    ),

    # ------------ Hardware control ------------
    # Suspend
    (['control', 'mod1'], 's', lazy.spawn('suspend')),
    # Reboot
    (['control', 'mod1'], 'r', lazy.spawn('reboot')),
    # Power off
    (['control', 'mod1'], 'p', lazy.spawn('poweroff')),
    # Volume
    ([], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +1%')),
    ([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -1%')),
    ([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    # Screen
    ([], 'XF86MonBrightnessUp', lazy.spawn('xbacklight -inc 5')),
    ([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 5')),
]
key_chords: List[KeyCmd] = [
    ([], 'w', lazy.spawn('firefox -new-window https://web.whatsapp.com')),
    ([], 'g', lazy.spawn('firefox -new-window https://mail.google.com/chat/u/1')),
    ([],'s',lazy.spawn('slack')),
    ([], 'c', lazy.spawn('code')),
    ([], 'k', lazy.spawn('firefox -new-window https://read.amazon.com')),
]

keys = [
    Key(cmd_keys, k, command) for cmd_keys, k, command in keys_cmds
]
keys.append(
    KeyChord(
        [mod],
        'p',
        [Key(cmd_keys, k, command) for cmd_keys, k, command in key_chords]
    )
)
for i, (name, _) in enumerate(groups_data):
    i = str(i + 1)
    keys.append(Key([mod], i, lazy.group[name].toscreen()))
    keys.append(Key([mod, 'shift'], i, lazy.window.togroup(name)))