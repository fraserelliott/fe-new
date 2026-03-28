from .base import Plugin
from .plugin_manager import PluginManager
from .fe_slate import FeSlatePlugin
from .react_router import ReactRouterPlugin
from .sequelize import SequelizePlugin

__all__ = [
    "Plugin",
    "PluginManager",
    "FeSlatePlugin",
    "ReactRouterPlugin",
    "SequelizePlugin"
]