from libqtile.config import Group
from libqtile.lazy import lazy


class GroupListAssembler(object):
    def __init__(self, group_names):
        self.group_names = group_names
        self.groups = [Group(name, **kwargs) for name, kwargs in self.group_names]

    def get_groups(self):
        return self.groups[:]

# keys = []
# groups = [Group(name, **kwargs) for name, kwargs in group_names]
# for i, (name, kwargs) in enumerate(group_names, 1):
#     # mod1 + number of group = switch to group
#     keys.append(
#         Key([mod], str(i), lazy.group[name].toscreen(), desc=f"Switch to group {name}")
#     )
#     # mod1 + shift + number of group = switch to & move focused window to group
#     keys.append(
#         Key(
#             [mod, "shift"], str(i), lazy.window.togroup(name),
#             desc=f"Switch to & move focused window to group {name}"
#         )
#     )