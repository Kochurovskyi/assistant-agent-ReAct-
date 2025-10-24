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
    config = {"configurable": {"thread_id": "1", "user_id": "Asis"}}
    # User input to create a profile memory
    input_messages = [HumanMessage(content="My name is Asis. I'm 34 years old, married with kids. I love sports, especially running and cycling.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    input_messages = [HumanMessage(content="I need to prepare for the upcoming marathon in 3 months and also help my son with his cycling competition.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    # User input to update instructions for creating ToDos
    input_messages = [HumanMessage(content="When creating or updating ToDo items, focus on sports training schedules and family activities.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    # User input for a ToDo
    input_messages = [HumanMessage(content="I need to schedule my weekly long runs and find a good cycling route for weekend training.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    # User input to update an existing ToDo
    input_messages = [HumanMessage(content="For the marathon training, I need to increase my weekly mileage gradually and add strength training.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    input_messages = [HumanMessage(content="I need to register my son for the youth cycling championship and get his bike serviced.")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()
    
    print("<<< Memories before the thread 2>>>")
    # Search for all memories across different namespaces
    user_id = "Asis"
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
    config = {"configurable": {"thread_id": "2", "user_id": "Asis"}}
    input_messages = [HumanMessage(content="I have 30 minutes, what tasks can I get done?")]
    async for chunk in graph.astream({"messages": input_messages}, config, stream_mode="values"): 
        chunk["messages"][-1].pretty_print()        
    
    input_messages = [HumanMessage(content="Yes, give me some options for my marathon training and my son's cycling preparation.")]
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

def test_production_agent():
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
    
    config = {"configurable": {"thread_id": "1", "user_id": "Asis"}}
    
    try:
        # User input to create a profile memory
        input_messages = [HumanMessage(content="My name is Asis. I'm 34 years old, married with kids. I love sports, especially running and cycling.")]
        for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        input_messages = [HumanMessage(content="I need to prepare for the upcoming marathon in 3 months and also help my son with his cycling competition.")]
        for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        # User input to update instructions for creating ToDos
        input_messages = [HumanMessage(content="When creating or updating ToDo items, focus on sports training schedules and family activities.")]
        for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        # User input for a ToDo
        input_messages = [HumanMessage(content="I need to schedule my weekly long runs and find a good cycling route for weekend training.")]
        for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        # User input to update an existing ToDo
        input_messages = [HumanMessage(content="For the marathon training, I need to increase my weekly mileage gradually and add strength training.")]
        for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        input_messages = [HumanMessage(content="I need to register my son for the youth cycling championship and get his bike serviced.")]
        for chunk in graph.stream({"messages": input_messages}, config, stream_mode="values"): 
            chunk["messages"][-1].pretty_print()
        
        print("\n" + "=" * 50)
        print("MEMORY VERIFICATION")
        print("=" * 50)
        
        # Search for all memories across different namespaces
        user_id = "Asis"
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
