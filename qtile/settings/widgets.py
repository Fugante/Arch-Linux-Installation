from libqtile import widget


def widget_defaults(font: str) -> dict:
    return {
        'font': font,
        'fontsize': 20,
        'padding': 3,
    }

def separator(foreground: str, background: str, padding: int) -> widget.Sep:
    return widget.Sep(
        foreground=foreground,
        background=background,
        linewidth=0,
        padding=padding
    )

def powerline_separator(foreground: str, background: str) -> widget.TextBox:
    return widget.TextBox(
        foreground=foreground,
        background=background,
        text='', # Icon: nf-oct-triangle_left
        fontsize=45,
        padding=-14
    )

def icon(foreground: str, background: str, fontsize: int, text: str) -> widget.TextBox:
    return widget.TextBox(
        foreground=foreground,
        background=background,
        fontsize=fontsize,
        text=text,
        padding=6
    )

def main_bar(colors: dict[str, str]):
    dark_separator = separator(colors['text'], colors['dark'], 5)
    return [
        dark_separator,
        widget.GroupBox(
            foreground=colors['light'],
            background=colors['dark'],
            fontsize=26,
            margin_y=3,
            margin_x=0,
            padding_y=8,
            padding_x=5,
            borderwidth=1,
            active=colors['active'],
            inactive=colors['inactive'],
            rounded=False,
            highlight_method='block',
            urgent_alert_method='block',
            urgent_border=colors['urgent'],
            this_current_screen_border=colors['focus'],
            this_screen_border=colors['grey'],
            other_current_screen_border=colors['dark'],
            other_screen_border=colors['dark'],
            disable_drag=True
        ),
        dark_separator,
        widget.Prompt(
            foreground=colors['light'],
            background=colors['dark'],
        ),
        widget.Spacer(
            background=colors['dark']
        ),
        powerline_separator(
            foreground=colors['color4'],
            background=colors['dark']
        ),
        widget.CurrentLayoutIcon(
            foreground=colors['light'],
            background=colors['color4'],
            scale=0.65
        ),
        widget.CurrentLayout(
            foreground=colors['light'],
            background=colors['color4'],
            padding=5
        ),
        powerline_separator(
            foreground=colors['color3'],
            background=colors['color4']
        ),
        # widget.Wlan(
        #     foreground=colors['text'],
        #     background=colors['color3'],
        #     interface='wlp1s0'
        # ),
        widget.Net(
            foreground=colors['text'],
            background=colors['color3'],
            interface='wlp1s0'
        ),
        powerline_separator(
            foreground=colors['color2'],
            background=colors['color3']
        ),
        icon(
            foreground=colors['text'],
            background=colors['color2'],
            fontsize=26,
            text=''
        ), # Icon: nf-mdi-memory
        widget.Memory(
            measure_mem='G',
            foreground=colors['text'],
            background=colors['color2'],
        ),
        widget.CPU(
            foreground=colors['text'],
            background=colors['color2'],
            format=' {freq_current}GHz {load_percent}%',
        ),
        powerline_separator(
            foreground=colors['color1'],
            background=colors['color2']
        ),
        widget.Battery(
            foreground=colors['text'],
            background=colors['color1'],
            format='{char} {percent:2.0%} {watt:.2f} W'
        ),
        powerline_separator(
            foreground=colors['color3'],
            background=colors['color1']
        ),
        icon(
            foreground=colors['text'],
            background=colors['color3'],
            text=' ',  # Icon: nf-mdi-calendar_clock
            fontsize=26
        ), 
        widget.Clock(
            foreground=colors['text'],
            background=colors['color3'],
            format='%A, %d %B %Y - %H:%M'
        ),
        powerline_separator(
            foreground=colors['color4'],
            background=colors['color3']
        ),
        widget.Systray(
            background=colors['color4'],
            icon_size=25,
            padding=5
        ),
        separator(
            foreground=colors['text'],
            background=colors['color4'],
            padding=10
        ),
    ]