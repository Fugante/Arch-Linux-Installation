from libqtile.config import Key, KeyChord
from libqtile.lazy import lazy


# mod = 'mod4'
class KeyListAssembler(object):
    def __init__(self, mod='mod4'):
        self.mod = mod
        self.keys = [
            Key(k[0], k[1], k[2]) for k in (
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

                # Change windows sizes (MonadTall and MonadWide
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

                # Restart Qtile
                ([mod, 'control'], 'r', lazy.restart()),

                # Shutdown Qtile
                ([mod, 'control'], 'q', lazy.shutdown()),

                # Spawn a command using a prompt widget
                ([mod], 'r', lazy.spawncmd()),

                # ----------- Application Keys -----------

                # Launch terminal
                ([mod], 'Return', lazy.spawn('alacritty')),

                # Print screen
                ([], 'Print', lazy.spawn(
                    "scrot '%Y-%m-%d_%wx$h.png' -e 'mv $f ~/Pictures/'"
                )),
                (['shift'], 'Print', lazy.spawn(
                    "scrot -s '%Y-%m-%d_%wx$h.png' -e 'mv $f ~/Pictures/'"
                )),
                ([mod], 'f', lazy.spawn('nautilus')),
                ([mod], 'b', lazy.spawn('google-chrome-stable')),

                # ------------ Hardware keys ------------

                # Suspend
                (['control', 'mod1'], 's', lazy.spawn('systemctl suspend')),

                # Reboot
                (['control', 'mod1'], 'r', lazy.spawn('reboot')),

                # Power off
                (['control', 'mod1'], 'p', lazy.spawn('poweroff')),

                # # Volume
                ([], 'XF86AudioRaiseVolume',
                    lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +1%')),
                ([], 'XF86AudioLowerVolume',
                    lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -1%')),
            )
        ]
        # Keychords
        self.keys.append(
            KeyChord(
                [mod], 'p', [
                    Key([], 'w',lazy.spawn(
                        'google-chrome-stable --app=https://web.whatsapp.com')),
                    Key([], 'g', lazy.spawn(
                        'google-chrome-stable --app=https://mail.google.com/chat/u/1')),
                    Key([], 's', lazy.spawn('slack')),
                    Key([], 'c', lazy.spawn('code')),
                    Key([], 'k', lazy.spawn(
                        'google-chrome-stable --app=https://read.amazon.com'
                    )),
                ]
            )
        )

    def add_group_keys(self, group_names):
        for i, (name, kwargs) in enumerate (group_names, 1):
            # mod1 + number of group = switch to group
            self.keys.append(Key([self.mod], str(i), lazy.group[name].toscreen()))
            # mod1 + shift + number of group = switch to & move focused window to group
            self.keys.append(Key([self.mod, 'shift'], str(i), lazy.window.togroup(name)))

    def get_keys(self):
        return self.keys[:]