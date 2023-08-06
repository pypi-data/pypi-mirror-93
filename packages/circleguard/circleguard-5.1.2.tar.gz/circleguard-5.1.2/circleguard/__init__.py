import logging

from circleguard.circleguard import Circleguard, KeylessCircleguard, set_options
from circleguard.loadables import (Replay, ReplayMap, ReplayPath, Map, User,
        MapUser, ReplayDir, ReplayContainer, Loadable, ReplayCache,
        CachedReplay, ReplayID, ReplayString, LoadableContainer)
from circleguard.mod import Mod
from circleguard.loader import (Loader, ReplayInfo, APIException,
        NoInfoAvailableException, UnknownAPIException, InternalAPIException,
        InvalidKeyException, RatelimitException, InvalidJSONException,
        ReplayUnavailableException)
from circleguard.version import __version__
from circleguard.investigator import Snap, Hit
from circleguard.span import Span
from circleguard.utils import (convert_statistic, order, Key,
        RatelimitWeight, TRACE, ColoredFormatter, replay_pairs, fuzzy_mods)
from circleguard.game_version import GameVersion, NoGameVersion
from circleguard.hitobjects import Hitobject, Circle, Slider, Spinner

logging.addLevelName(TRACE, "TRACE")
formatter = ColoredFormatter("[%(threadName)s][%(name)s][%(levelname)s]  %(message)s  (%(filename)s:%(lineno)s)")
handler_stream = logging.StreamHandler()
handler_stream.setFormatter(formatter)
logging.getLogger("circleguard").addHandler(handler_stream)

# don't expose ColoredFormatter to consumers
del ColoredFormatter

__all__ = [
# core
"Circleguard", "KeylessCircleguard", "set_options",
# loadables
"ReplayContainer", "Map", "User", "MapUser",
"ReplayCache", "Replay", "ReplayMap", "ReplayPath", "CachedReplay", "Loadable",
"ReplayID", "ReplayDir", "ReplayString", "LoadableContainer",
# enums
"Key", "RatelimitWeight",
# mod
"Mod",
# utils
"convert_statistic", "order", "Key", "RatelimitWeight", "TRACE", "replay_pairs",
"fuzzy_mods",
# loader
"Loader", "ReplayInfo",
# exceptions
"APIException",
"NoInfoAvailableException", "UnknownAPIException", "InternalAPIException",
"InvalidKeyException", "RatelimitException", "InvalidJSONException",
"ReplayUnavailableException",
# version
"__version__",
# investigation-related classes
"Snap", "Hit",
# span
"Span",
# GameVersion
"GameVersion", "NoGameVersion",
# hitobjects
"Hitobject", "Circle", "Slider", "Spinner"
]
