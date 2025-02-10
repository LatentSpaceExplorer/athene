from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import List, Type
from src.plugins.base import Plugin

class ChatModel:
    def __init__(self, plugin_classes: List[Type[Plugin]]):
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
        
        # Initialize plugins
        self.plugins = {
            plugin_class().name: plugin_class() 
            for plugin_class in plugin_classes
        }
        
        # Get tools from all plugins
        self.tools = []
        for plugin in self.plugins.values():
            self.tools.extend(plugin.get_tools())
        
        # Bind tools to the LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Create prompt template
        template = """You are Athene, a helpful AI assistant who can 
        manage a to-do list, 
        read clipboard content, 
        and engage in general conversation.

        Your responses should be friendly and personable, while remaining efficient and clear.

        If the user's input is related to task management, use the appropriate tool.
        If the user wants to read clipboard content, use the ReadClipboard tool.
        
        If it's general conversation, respond naturally while maintaining your identity as Athene.

        User Input: {user_input}
        """
        
        self.prompt = ChatPromptTemplate.from_template(template)
    
    async def get_response(self, text: str) -> str:
        try:
            response = await self.llm_with_tools.ainvoke(
                self.prompt.format_messages(user_input=text)
            )
            
            # If the response contains tool calls, execute the tool
            if response.tool_calls:
                tool_call = response.tool_calls[0]
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                # Determine which plugin should handle the tool
                for plugin in self.plugins.values():
                    if any(tool.__name__ == tool_name for tool in plugin.get_tools()):
                        return plugin.execute_tool(tool_name, **tool_args)
                
                return "I couldn't find the appropriate tool for that action."
            
            # If the response doesn't contain tool calls, return the response
            return response.content or "I couldn't process that request."
            
        except Exception as e:
            print(f"[Error] {str(e)}")
            return "An error occurred processing your request"