"""Test functions for the memory agent."""
import asyncio
import pytest
from langchain_core.messages import HumanMessage
from graph.builder import graph

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_memory_agent():
    """Comprehensive test of the memory agent functionality"""
    
    print("=" * 80)
    print("MEMORY AGENT COMPREHENSIVE TESTING")
    print("=" * 80)
    
    # Test 1: Create user profile
    print("\n" + "=" * 50)
    print("TEST 1: Creating User Profile")
    print("=" * 50)
    
    # We supply a thread ID for short-term (within-thread) memory
    # We supply a user ID for long-term (across-thread) memory 
    config = {"configurable": {"thread_id": "1", "user_id": "Lance"}}
    # User input to create a profile memory
    input_messages = [HumanMessage(content="My name is Lance. I live in SF with my wife. I have a 1 year old daughter.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    input_messages = [HumanMessage(content="My wife asked me to book swim lessons for the baby.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    # User input to update instructions for creating ToDos
    input_messages = [HumanMessage(content="When creating or updating ToDo items, include specific local businesses / vendors.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    # User input for a ToDo
    input_messages = [HumanMessage(content="I need to fix the jammed electric Yale lock on the door.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    # User input to update an existing ToDo
    input_messages = [HumanMessage(content="For the swim lessons, I need to get that done by end of November.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    input_messages = [HumanMessage(content="Need to call back City Toyota to schedule car service.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    print("<<< Memories before the thread 2>>>")
    # Search for all memories across different namespaces
    user_id = "Lance"
    todo_category = "general"
    
    # Search profile memories
    profile_namespace = ("profile", todo_category, user_id)
    profile_memories = graph.store.search(profile_namespace)
    print("Profile memories:")
    for m in profile_memories:  
        print(f"Profile: {m.value}")
    
    # Search todo memories
    todo_namespace = ("todo", todo_category, user_id)
    todo_memories = graph.store.search(todo_namespace)
    print("Todo memories:")
    for m in todo_memories: 
        print(f"Todo: {m.value}")
    
    # Search instruction memories
    instructions_namespace = ("instructions", todo_category, user_id)
    instruction_memories = graph.store.search(instructions_namespace)
    print("Instruction memories:")
    for m in instruction_memories:  
        print(f"Instructions: {m.value}")

    print('_'*20)
    print('MEmo after the 2nd thread:')
    # We supply a thread ID for short-term (within-thread) memory
    # We supply a user ID for long-term (across-thread) memory 
    config = {"configurable": {"thread_id": "2", "user_id": "Lance"}}
    input_messages = [HumanMessage(content="I have 30 minutes, what tasks can I get done?")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()        
    
    input_messages = [HumanMessage(content="Yes, give me some options to call for swim lessons.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()

    print("Profile memories:")
    for m in profile_memories:  
        print(f"Profile: {m.value}")
    
    # Search todo memories
    todo_namespace = ("todo", todo_category, user_id)
    todo_memories = graph.store.search(todo_namespace)
    print("Todo memories:")
    for m in todo_memories: 
        print(f"Todo: {m.value}")
    
    # Search instruction memories
    instructions_namespace = ("instructions", todo_category, user_id)
    instruction_memories = graph.store.search(instructions_namespace)
    print("Instruction memories:")
    for m in instruction_memories:  
        print(f"Instructions: {m.value}")

@pytest.mark.asyncio
async def test_production_agent():
    """Production-ready test of the memory agent functionality"""
    
    print("=" * 80)
    print("PRODUCTION MEMORY AGENT TESTING")
    print("=" * 80)
    
    # Health check
    print("\n" + "=" * 50)
    print("HEALTH CHECK")
    print("=" * 50)
    from graph.builder import health_check, get_metrics
    
    health_status = health_check()
    print(f"Health Status: {health_status['status']}")
    print(f"Store Connectivity: {health_status['store_connectivity']}")
    
    # Test 1: Create user profile
    print("\n" + "=" * 50)
    print("TEST 1: Creating User Profile")
    print("=" * 50)
    
    config = {"configurable": {"thread_id": "1", "user_id": "Lance"}}
    
    try:
        # User input to create a profile memory
        input_messages = [HumanMessage(content="My name is Lance. I live in SF with my wife. I have a 1 year old daughter.")]
        async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        input_messages = [HumanMessage(content="My wife asked me to book swim lessons for the baby.")]
        async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        # User input to update instructions for creating ToDos
        input_messages = [HumanMessage(content="When creating or updating ToDo items, include specific local businesses / vendors.")]
        async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        # User input for a ToDo
        input_messages = [HumanMessage(content="I need to fix the jammed electric Yale lock on the door.")]
        async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        # User input to update an existing ToDo
        input_messages = [HumanMessage(content="For the swim lessons, I need to get that done by end of November.")]
        async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        input_messages = [HumanMessage(content="Need to call back City Toyota to schedule car service.")]
        async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        print("\n" + "=" * 50)
        print("MEMORY VERIFICATION")
        print("=" * 50)
        
        # Search for all memories across different namespaces
        user_id = "Lance"
        todo_category = "general"
        
        # Search profile memories
        profile_namespace = ("profile", todo_category, user_id)
        profile_memories = graph.store.search(profile_namespace)
        print("Profile memories:")
        for m in profile_memories:  
            print(f"Profile: {m.value}")
        
        # Search todo memories
        todo_namespace = ("todo", todo_category, user_id)
        todo_memories = graph.store.search(todo_namespace)
        print("Todo memories:")
        for m in todo_memories: 
            print(f"Todo: {m.value}")
        
        # Search instruction memories
        instructions_namespace = ("instructions", todo_category, user_id)
        instruction_memories = graph.store.search(instructions_namespace)
        print("Instruction memories:")
        for m in instruction_memories:  
            print(f"Instructions: {m.value}")
        
        print("\n" + "=" * 50)
        print("FINAL METRICS")
        print("=" * 50)
        final_metrics = get_metrics()
        print(f"Total Requests: {final_metrics['requests_total']}")
        print(f"Total Errors: {final_metrics['errors_total']}")
        print(f"Memory Updates: {final_metrics['memory_updates']}")
        print(f"Average Response Time: {final_metrics['avg_response_time']:.2f}s")
        print(f"Error Rate: {final_metrics['error_rate']:.2%}")
        
        print("\n" + "=" * 50)
        print("PRODUCTION TEST COMPLETED SUCCESSFULLY")
        print("=" * 50)
        
    except Exception as e:
        from utils.logging_config import logger
        logger.error(f"Production test failed: {e}")
        print(f"Test failed with error: {e}")
        raise
