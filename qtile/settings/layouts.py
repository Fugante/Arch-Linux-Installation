from libqtile import layout


def init_layouts(colors):
    layout_conf = {
        'border_focus': colors['focus'][0],
        'border_width': 1,
        'margin': 4,
    }
    return [
        layout.Max(),
        layout.MonadTall(
            ratio=0.6,
            **layout_conf
        ),
        layout.MonadWide(
            ratio=0.6,
            **layout_conf,
        ),
    ]