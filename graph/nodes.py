"""Node functions for the memory agent graph."""
import asyncio
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

# Async helper function for memory retrieval
async def _search_memory_async(store: BaseStore, namespace):
    """Async wrapper for store search operations."""
    # Since BaseStore doesn't have async methods, we'll use asyncio.to_thread
    # to run the sync operation in a thread pool
    return await asyncio.to_thread(store.search, namespace)

async def task_asis(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Load memories from the store and use them to personalize the chatbot's response."""
    start_time = time.time()
    
    try:
        logger.info("Starting task_asis processing")
        
        # Get the user ID from the config
        configurable = Configuration.from_runnable_config(config)
        user_id = configurable.user_id
        todo_category = configurable.todo_category
        task_asis_role = configurable.task_asis_role

        # Parallel memory retrieval using asyncio.gather()
        profile_namespace = ("profile", todo_category, user_id)
        todo_namespace = ("todo", todo_category, user_id)
        instructions_namespace = ("instructions", todo_category, user_id)
        
        # Create async tasks for parallel execution
        profile_task = asyncio.create_task(_search_memory_async(store, profile_namespace))
        todo_task = asyncio.create_task(_search_memory_async(store, todo_namespace))
        instructions_task = asyncio.create_task(_search_memory_async(store, instructions_namespace))
        
        # Wait for all memory retrievals to complete
        profile_memories, todo_memories, instructions_memories = await asyncio.gather(
            profile_task, todo_task, instructions_task
        )
        
        # Process profile memory
        if profile_memories:
            user_profile = profile_memories[0].value
            logger.info(f"Retrieved profile for user {user_id}")
        else:
            user_profile = None
            logger.info(f"No profile found for user {user_id}")

        # Process todo memory
        todo = "\n".join(f"{mem.value}" for mem in todo_memories)
        logger.info(f"Retrieved {len(todo_memories)} todo items for user {user_id}")

        # Process instructions memory
        if instructions_memories:
            instructions = instructions_memories[0].value
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

        # Async LLM invocation
        response = await model.bind_tools([UpdateMemory], parallel_tool_calls=False).ainvoke(
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

async def update_profile(state: MessagesState, config: RunnableConfig, store: BaseStore):
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

        # Retrieve the most recent memories for context (async)
        existing_items = await asyncio.to_thread(store.search, namespace)
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

        # Async extractor invocation
        result = await asyncio.to_thread(profile_extractor.invoke, {
            "messages": updated_messages, 
            "existing": existing_memories
        })

        # Save the memories from Trustcall to the store (async)
        import uuid
        for r, rmeta in zip(result["responses"], result["response_metadata"]):
            await asyncio.to_thread(store.put,
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

async def update_todos(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    
    # Get the user ID from the config
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    todo_category = configurable.todo_category

    # Define the namespace for the memories
    namespace = ("todo", todo_category, user_id)

    # Retrieve the most recent memories for context (async)
    existing_items = await asyncio.to_thread(store.search, namespace)

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

    # Async extractor invocation
    result = await asyncio.to_thread(todo_extractor.invoke, {
        "messages": updated_messages, 
        "existing": existing_memories
    })

    # Save the memories from Trustcall to the store (async)
    import uuid
    for r, rmeta in zip(result["responses"], result["response_metadata"]):
        await asyncio.to_thread(store.put,
            namespace,
            rmeta.get("json_doc_id", str(uuid.uuid4())),
            r.model_dump(mode="json"),
        )
        
    # Respond to the tool call made in task_asis, confirming the update    
    tool_calls = state['messages'][-1].tool_calls

    # Extract the changes made by Trustcall and add the the ToolMessage returned to task_asis
    todo_update_msg = extract_tool_info(sniffer.called_tools, tool_name)
    return {"messages": [{"role": "tool", "content": todo_update_msg, "tool_call_id": tool_calls[0]['id']}]}

async def update_instructions(state: MessagesState, config: RunnableConfig, store: BaseStore):
    """Reflect on the chat history and update the memory collection."""
    
    # Get the user ID from the config
    configurable = Configuration.from_runnable_config(config)
    user_id = configurable.user_id
    todo_category = configurable.todo_category
    
    namespace = ("instructions", todo_category, user_id)

    existing_memory = await asyncio.to_thread(store.get, namespace, "user_instructions")
        
    # Format the memory in the system prompt
    system_msg = CREATE_INSTRUCTIONS.format(current_instructions=existing_memory.value if existing_memory else None)
    new_memory = await model.ainvoke([SystemMessage(content=system_msg)] + state['messages'][:-1] + [HumanMessage(content="Please update the instructions based on the conversation")])

    # Overwrite the existing memory in the store (async)
    key = "user_instructions"
    await asyncio.to_thread(store.put, namespace, key, {"memory": new_memory.content})
    tool_calls = state['messages'][-1].tool_calls
    # Return tool message with update verification
    return {"messages": [{"role": "tool", "content": "updated instructions", "tool_call_id": tool_calls[0]['id']}]}
