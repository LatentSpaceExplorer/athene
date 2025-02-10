from .base import Plugin
from pydantic import BaseModel
import pyperclip


class ReadClipboard(BaseModel):
    """Read and process text from the clipboard."""


class ClipboardPlugin(Plugin):
    @property
    def name(self) -> str:
        return "clipboard reader"

    def get_tools(self):
        return [ReadClipboard]
    
    def execute_tool(self, tool_name: str, **kwargs) -> str:
        if tool_name == "ReadClipboard":
            return self._read_clipboard()
        raise ValueError(f"Unknown tool: {tool_name}")
    
    def _read_clipboard(self) -> str:
        text = pyperclip.paste()
        if not text:
            return "The clipboard is empty."
        return f"Here's the text from your clipboard: {text}" 