from libqtile import widget


class WidgetListAssembler(object):
    def __init__(self, colors, font):
        self.colors = colors
        self.font = font

    def widget_defaults(self):
        return {
            'font': self.font,
            'fontsize': 20,
            'padding': 3,
        }

    def separator(self, fg='text', bg='dark', padding=5):
        return widget.Sep(
        foreground=self.colors[fg],
        background=self.colors[bg],
        linewidth=0,
        padding=padding
    )

    def powerline(self, fg='light', bg='dark'):
        return widget.TextBox(
            foreground=self.colors[fg],
            background=self.colors[bg],
            text='', # Icon: nf-oct-triangle_left
            fontsize=80,
            padding=-12
        )

    def icon(self, fg='text', bg='dark', fontsize=16, text="?"):
        return widget.TextBox(
            foreground=self.colors[fg],
            background=self.colors[bg],
            fontsize=fontsize,
            text=text,
            padding=6
        )

    def primary_widgets(self):
        return [
            self.separator(),
            widget.GroupBox(
                foreground=self.colors['light'],
                background=self.colors['dark'],
                fontsize=40,
                margin_y=3,
                margin_x=0,
                padding_y=8,
                padding_x=5,
                borderwidth=1,
                active=self.colors['active'],
                inactive=self.colors['inactive'],
                rounded=False,
                highlight_method='block',
                urgent_alert_method='block',
                urgent_border=self.colors['urgent'],
                this_current_screen_border=self.colors['focus'],
                this_screen_border=self.colors['grey'],
                other_current_screen_border=self.colors['dark'],
                other_screen_border=self.colors['dark'],
                disable_drag=True
            ),
            self.separator(),
            widget.Prompt(
                foreground=self.colors['light'],
                background=self.colors['dark'],
            ),
            widget.Spacer(
                background=self.colors['dark']
            ),
            self.powerline('color4', 'dark'),
            widget.CurrentLayoutIcon(
                foreground=self.colors['light'],
                background=self.colors['color4'],
                scale=0.65
            ),
            widget.CurrentLayout(
                foreground=self.colors['light'],
                background=self.colors['color4'],
                padding=5
            ),
            self.powerline('color3', 'color4'),
            widget.Net(
                foreground=self.colors['text'],
                background=self.colors['color3'],
                interface='enp6s0'
            ),
            self.powerline('color2', 'color3'),
            self.icon(bg="color2", text='', fontsize=40), # Icon: nf-mdi-memory
            widget.Memory(
                foreground=self.colors['text'],
                background=self.colors['color2'],
            ),
            widget.CPU(
                foreground=self.colors['text'],
                background=self.colors['color2'],
                format=' {freq_current}GHz {load_percent}%',
            ),
            self.powerline('color1', 'color2'),
            self.icon(bg='color1', fontsize=40, text=' '), # Icon: nf-mdi-calendar_clock
            widget.Clock(
                foreground=self.colors['text'],
                background=self.colors['color1'],
                format='%A, %d %B %Y, %H:%M'
            ),
            self.powerline('color4', 'color1'),
            widget.Systray(
                background=self.colors['color4'],
                icon_size=25,
                padding=5
            ),
            self.separator(bg='color4', padding=10),
        ]