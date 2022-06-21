from typing import Dict, List, Tuple

from libqtile.config import Group


group = Tuple[str, Dict]

# Icons were downloaded from https://www.nerdfonts.com/cheat-sheet
groups_data: Tuple[group] = (
    ('', {'layout': 'max'}),           # nf-dev-terminal
    ('', {'layout': 'max'}),           # nf-fae-python
    ('', {'layout': 'monadtall'}),     # nf-dev-chrome
    ('', {'layout': 'max'}),           # nf-fa-slack
    ('', {'layout': 'monadtall'}),     # nf-fa-whatsapp
)
groups: List[Group] = [Group(name, **kwargs) for name, kwargs in groups_data]