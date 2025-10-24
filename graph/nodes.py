"""Node functions for the memory agent graph."""
import time
import traceback
from datetime import datetime
from typing import Literal

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import merge_message_runs, SystemMessage, HumanMessage
from langgraph.graph import MessagesState
from langgraph.store.base import BaseStore

from config import Configuration
from utils.logging_config import logger
from utils.metrics import metrics
from utils.helpers import Sniffer, extract_tool_info
from chains.prompts import MODEL_SYSTEM_MESSAGE, TRUSTCALL_INSTRUCTION, CREATE_INSTRUCTIONS
from chains.extractors import initialize_model, create_profile_extractor, create_todo_extractor
from schemas.memory import UpdateMemory

# Initialize model and extractors
model = initialize_model()
profile_extractor = create_profile_extractor(model)

def task_asis(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Load memories from the store and use them to personalize the chatbot's response."""
    start_time = time.time()
    
    try:
        logger.info("Starting task_asis processing")
        
        # Get the user ID from the config
        configurable = Configuration.from_runnable_config(config)
        user_id = configurable.user_id
        todo_category = configurable.todo_category
        task_asis_role = configurable.task_asis_role

        # Retrieve profile memory from the store
        namespace = ("profile", todo_category, user_id)
        memories = store.search(namespace)
        if memories:
            user_profile = memories[0].value
            logger.info(f"Retrieved profile for user {user_id}")
        else:
            user_profile = None
            logger.info(f"No profile found for user {user_id}")

        # Retrieve todo memory from the store
        namespace = ("todo", todo_category, user_id)
        memories = store.search(namespace)
        todo = "\n".join(f"{mem.value}" for mem in memories)
        logger.info(f"Retrieved {len(memories)} todo items for user {user_id}")

        # Retrieve custom instructions
        namespace = ("instructions", todo_category, user_id)
        memories = store.search(namespace)
        if memories:
            instructions = memories[0].value
            logger.info(f"Retrieved instructions for user {user_id}")
        else:
            instructions = ""
            logger.info(f"No instructions found for user {user_id}")
        
        system_msg = MODEL_SYSTEM_MESSAGE.format(
            task_asis_role=task_asis_role, 
            user_profile=user_profile, 
            todo=todo, 
            instructions=instructions
        )

        # Respond using memory as well as the chat history
        response = model.bind_tools([UpdateMemory], parallel_tool_calls=False).invoke(
            [SystemMessage(content=system_msg)] + state["messages"]
        )
        
        response_time = time.time() - start_time
        metrics.record_request(response_time)
        logger.info(f"task_asis completed in {response_time:.2f}s")
        
        return {"messages": [response]}
        
    except Exception as e:
        logger.error(f"Error in task_asis: {e}")
        logger.error(traceback.format_exc())
        metrics.record_error()
        raise

def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    start_time = time.time()
    
    try:
        logger.info("Starting profile update")
        
        # Get the user ID from the config
        configurable = Configuration.from_runnable_config(config)
        user_id = configurable.user_id
        todo_category = configurable.todo_category

        # Define the namespace for the memories
        namespace = ("profile", todo_category, user_id)

        # Retrieve the most recent memories for context
        existing_items = store.search(namespace)
        logger.info(f"Found {len(existing_items)} existing profile items for user {user_id}")

        # Format the existing memories for the Trustcall extractor
        tool_name = "Profile"
        existing_memories = ([(existing_item.key, tool_name, existing_item.value)
                              for existing_item in existing_items]
                              if existing_items
                              else None
                            )

        # Merge the chat history and the instruction
        TRUSTCALL_INSTRUCTION_FORMATTED = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
        updated_messages = list(merge_message_runs(
            messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION_FORMATTED)] + state["messages"][:-1]
        ))

        # Invoke the extractor
        result = profile_extractor.invoke({
            "messages": updated_messages, 
            "existing": existing_memories
        })

        # Save the memories from Trustcall to the store
        import uuid
        for r, rmeta in zip(result["responses"], result["response_metadata"]):
            store.put(
                namespace,
                rmeta.get("json_doc_id", str(uuid.uuid4())),
                r.model_dump(mode="json"),
            )
        
        metrics.record_memory_update()
        response_time = time.time() - start_time
        logger.info(f"Profile update completed in {response_time:.2f}s")
        
        tool_calls = state['messages'][-1].tool_calls
        return {"messages": [{"role": "tool", "content": "updated profile", "tool_call_id": tool_calls[0]['id']}]}
        
    except Exception as e:
        logger.error(f"Error in update_profile: {e}")
        logger.error(traceback.format_exc())
        metrics.record_error()
        raise

def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    
    # Get the user ID from the config
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    todo_category = configurable.todo_category

    # Define the namespace for the memories
    namespace = ("todo", todo_category, user_id)

    # Retrieve the most recent memories for context
    existing_items = store.search(namespace)

    # Format the existing memories for the Trustcall extractor
    tool_name = "ToDo"
    existing_memories = ([(existing_item.key, tool_name, existing_item.value)
                          for existing_item in existing_items]
                          if existing_items
                          else None
                        )

    # Merge the chat history and the instruction
    TRUSTCALL_INSTRUCTION_FORMATTED = TRUSTCALL_INSTRUCTION.format(time=datetime.now().isoformat())
    updated_messages = list(merge_message_runs(
        messages=[SystemMessage(content=TRUSTCALL_INSTRUCTION_FORMATTED)] + state["messages"][:-1]
    ))

    # Initialize the sniffer for visibility into the tool calls made by Trustcall
    sniffer = Sniffer()
    
    # Create the Trustcall extractor for updating the ToDo list 
    todo_extractor = create_todo_extractor(model, tool_name).with_listeners(on_end=sniffer)

    # Invoke the extractor
    result = todo_extractor.invoke({
        "messages": updated_messages, 
        "existing": existing_memories
    })

    # Save the memories from Trustcall to the store
    import uuid
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        store.put(
            namespace,
            rmeta.get("json_doc_id", str(uuid.uuid4())),
            r.model_dump(mode="json"),
        )
        
    # Respond to the tool call made in task_asis, confirming the update    
    tool_calls = state['messages'][-1].tool_calls

    # Extract the changes made by Trustcall and add the the ToolMessage returned to task_asis
    todo_update_msg = extract_tool_info(sniffer.called_tools, tool_name)
    return {"messages": [{"role": "tool", "content": todo_update_msg, "tool_call_id": tool_calls[0]['id']}]}

def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    
    # Get the user ID from the config
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    todo_category = configurable.todo_category
    
    namespace = ("instructions", todo_category, user_id)

    existing_memory = store.get(namespace, "user_instructions")
        
    # Format the memory in the system prompt
    system_msg = CREATE_INSTRUCTIONS.format(current_instructions=existing_memory.value if existing_memory else None)
    new_memory = model.invoke([SystemMessage(content=system_msg)] + state['messages'][:-1] + [HumanMessage(content="Please update the instructions based on the conversation")])

    # Overwrite the existing memory in the store 
    key = "user_instructions"
    store.put(namespace, key, {"memory": new_memory.content})
    tool_calls = state['messages'][-1].tool_calls
    # Return tool message with update verification
    return {"messages": [{"role": "tool", "content": "updated instructions", "tool_call_id": tool_calls[0]['id']}]}
