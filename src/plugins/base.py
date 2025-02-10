from abc import ABC, abstractmethod

class Plugin(ABC):
    """Base class for all plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the plugin"""
        pass

    @abstractmethod
    def get_tools(self):
        """Return the tools this plugin provides"""
        pass

    @abstractmethod
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute a tool provided by this plugin"""
        pass 