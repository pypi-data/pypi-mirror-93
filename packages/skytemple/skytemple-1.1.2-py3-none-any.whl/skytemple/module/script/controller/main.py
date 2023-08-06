#  Copyright 2020-2021 Parakoopa and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.

from skytemple.core.module_controller import NotImplementedController


from gi.repository import Gtk

from skytemple.core.abstract_module import AbstractModule
from skytemple.core.module_controller import SimpleController

SCRIPT_SCENES = 'Script Scenes'


class MainController(SimpleController):
    def __init__(self, module: AbstractModule, item_id: int):
        pass

    def get_title(self) -> str:
        return SCRIPT_SCENES

    def get_content(self) -> Gtk.Widget:
        return self.generate_content_label(
            "This section lets you edit overworld scenes in the game, so anything that happens outside of Dungeons.\n"
            "This also includes cutscene visuals and some system related scenes, "
            "like credits or the title screen logos."
        )

    def get_icon(self) -> str:
        return 'skytemple-illust-scenes'
