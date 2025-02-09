from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
# from langchain_core.tools import Tool
from typing import List, Optional
from pydantic import BaseModel, Field
import pyperclip


# Define Pydantic models for our tools
class AddTask(BaseModel):
    """Add a new task to the todo list."""
    task_description: str = Field(..., description="The description of the task to add")
    due_date: Optional[str] = Field(None, description="Optional due date for the task")

class DeleteTask(BaseModel):
    """Delete a task from the todo list."""
    task_id: int = Field(..., description="The ID (1-based index) of the task to delete")

class ListTasks(BaseModel):
    """List all tasks in the todo list."""
    pass

class ReadClipboard(BaseModel):
    """Read and process text from the clipboard."""
    pass

class ChatModel:
    def __init__(self, todo_manager):
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
        self.todo_manager = todo_manager
        
        # Define tools properly using Tool class
        self.tools = [AddTask, DeleteTask, ListTasks, ReadClipboard]
        
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
        
    def _add_task(self, task_description: str, due_date: Optional[str] = None) -> str:

        return self.todo_manager.add_todo(task_description, due_date)
    
    def _delete_task(self, task_id: int) -> str:
        return self.todo_manager.remove_todo(task_id - 1)
    
    def _list_tasks(self) -> str:
        print("[ChatModel] listing tasks")
        return self.todo_manager.list_todos()
    
    def _read_clipboard(self) -> str:
        text = pyperclip.paste()
        if not text:
            return "The clipboard is empty."
        return f"Here's the text from your clipboard: {text}"
    
    async def get_response(self, text: str) -> str:
        try:
            # Invoke the LLM with tools
            response = await self.llm_with_tools.ainvoke(
                self.prompt.format_messages(user_input=text)
            )

            print("[ChatModel] response: ", response)
            
            # If there are tool calls, process them
            if response.tool_calls:

                tool_call = response.tool_calls[0]

                tool_name = tool_call['name']
                tool_args = tool_call['args']

                # Execute the appropriate tool function
                if tool_name == "AddTask":
                    return self._add_task(**tool_args)
                elif tool_name == "DeleteTask":
                    return self._delete_task(**tool_args)
                elif tool_name == "ListTasks":
                    return self._list_tasks()
                elif tool_name == "ReadClipboard":
                    return self._read_clipboard()
                
                return "I couldn't find the appropriate tool for that action."
            
            # If no tool calls, return the regular response
            return response.content or "I couldn't process that request."
            
        except Exception as e:
            print(f"[Error] {str(e)}")
            return "An error occurred processing your request"