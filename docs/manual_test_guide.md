# Manual Testing Guide for FastAPI Memory Agent Server

## 🚀 Server Status
The FastAPI server should be running at: **http://localhost:8000**

## 🎯 Comprehensive Conversation Simulation Testing

### Overview
This guide provides a systematic approach to test the memory agent through realistic conversation simulations, checking memory state after each message to evaluate system performance.

### Testing Methodology
1. **10-Message Conversation**: Simulate realistic user interaction
2. **Memory State Tracking**: Check memory after each message
3. **Detailed Record Analysis**: Examine data quality and consistency
4. **Performance Evaluation**: Assess system strengths and weaknesses

## 📋 Testing Checklist

### 1. Basic Server Health Check

**Test the root endpoint:**
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Asis Memory Agent API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc",
  "health": "/api/v1/health",
  "metrics": "/api/v1/metrics",
  "websocket": "/ws/chat"
}
```

### 2. Health Check Endpoint

**Test health status:**
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-24T...",
  "store_connectivity": "ok",
  "metrics": {
    "requests_total": 0,
    "errors_total": 0,
    "memory_updates": 0,
    "avg_response_time": 0,
    "error_rate": 0.0
  }
}
```

### 3. Metrics Endpoint

**Test metrics:**
```bash
curl http://localhost:8000/api/v1/metrics
```

**Expected Response:**
```json
{
  "requests_total": 0,
  "errors_total": 0,
  "memory_updates": 0,
  "avg_response_time": 0,
  "error_rate": 0.0
}
```

### 4. Chat Endpoint Testing

**Test basic chat:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! I am Asis, 34 years old, married with kids. I love sports, especially running and cycling.",
    "user_id": "Asis",
    "session_id": "test-session-1"
  }'
```

**Expected Response:**
```json
{
  "response": "Hello Asis! I've updated my memory with your profile information...",
  "session_id": "test-session-1",
  "user_id": "Asis",
  "metadata": {
    "model": "gemini-2.5-flash-lite",
    "timestamp": "...",
    "thread_id": "test-session-1"
  }
}
```

### 5. Memory Management Testing

**Get user profile:**
```bash
curl "http://localhost:8000/api/v1/memories/profile/Asis"
```

**Get user todos:**
```bash
curl "http://localhost:8000/api/v1/memories/todos/Asis"
```

**Get user instructions:**
```bash
curl "http://localhost:8000/api/v1/memories/instructions/Asis"
```

### 6. Comprehensive 10-Message Conversation Simulation

**Test Setup:**
```bash
# Set user ID for testing
USER_ID="test-user"
```

**Message 1: Basic Introduction**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi! I am Emma, a 32-year-old software engineer.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-1"
  }'
```

**Check Memory State After Message 1:**
```bash
curl "http://localhost:8000/api/v1/memories/all/$USER_ID" | jq '.'
```

**Message 2: Add Location**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I live in Seattle and work remotely for a tech company.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-2"
  }'
```

**Check Memory State After Message 2:**
```bash
curl "http://localhost:8000/api/v1/memories/all/$USER_ID" | jq '.'
```

**Message 3: Add Interests**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I love hiking, photography, and cooking Italian food in my spare time.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-3"
  }'
```

**Check Memory State After Message 3:**
```bash
curl "http://localhost:8000/api/v1/memories/all/$USER_ID" | jq '.'
```

**Message 4: Add Tasks**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need to plan a hiking trip to Mount Rainier next month and organize my photography portfolio.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-4"
  }'
```

**Check Memory State After Message 4:**
```bash
curl "http://localhost:8000/api/v1/memories/all/$USER_ID" | jq '.data | {profiles: .profiles | length, todos: .todos | length, instructions: .instructions | length}'
```

**Message 5: Add More Tasks**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I also want to learn Spanish and start a fitness routine. Can you help me plan these?",
    "user_id": "'$USER_ID'",
    "session_id": "conv-5"
  }'
```

**Message 6: Add Instructions**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "When creating todos, always set a priority level (high, medium, low) and include a deadline. I prefer detailed task descriptions.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-6"
  }'
```

**Message 7: Update Profile**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I moved to Portland last month and now work as a senior software engineer at a tech startup.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-7"
  }'
```

**Message 8: Add More Tasks**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need to book a dentist appointment for next week and organize my home office.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-8"
  }'
```

**Message 9: Test Memory Recall**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What do you remember about me? What are my current tasks?",
    "user_id": "'$USER_ID'",
    "session_id": "conv-9"
  }'
```

**Message 10: Add Interest**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I also enjoy rock climbing and have been doing it for 2 years.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-10"
  }'
```

**Message 11: Add Complex Task**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I need to plan a photography workshop for beginners next month. This is high priority and needs to be completed by December 15th.",
    "user_id": "'$USER_ID'",
    "session_id": "conv-11"
  }'
```

**Message 12: Final Test**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Can you summarize everything you know about me and my current tasks?",
    "user_id": "'$USER_ID'",
    "session_id": "conv-12"
  }'
```

**Final Memory State Check:**
```bash
curl "http://localhost:8000/api/v1/memories/all/$USER_ID" | jq '.'
```

## 📊 Test Results Analysis

### Expected Results After 12 Messages:
- **Profiles**: 1 (updated, not duplicated)
- **Todos**: 6-8 (with priorities and deadlines)
- **Instructions**: 1 (properly applied to new todos)

### Performance Evaluation Criteria:

#### ✅ **What Should Work Well:**
1. **Todo Creation**: Detailed tasks with solutions and time estimates
2. **Memory Persistence**: Data persists across all messages
3. **User Isolation**: Each user maintains separate memory space
4. **API Performance**: Fast response times (< 2 seconds)

#### ⚠️ **Common Issues Found:**
1. **Profile Updates**: May create duplicate profiles instead of updating
2. **Instruction Application**: User preferences not applied to new todos
3. **Priority/Deadline Setting**: Instructions not being followed
4. **Data Quality**: Some encoding issues in solutions

### Success Metrics:
- **Profile Management**: ⭐⭐⭐⭐⭐ (Perfect) / ⭐⭐⭐ (Good) / ⭐⭐ (Poor)
- **Todo Management**: ⭐⭐⭐⭐⭐ (Perfect) / ⭐⭐⭐ (Good) / ⭐⭐ (Poor)
- **Instruction Application**: ⭐⭐⭐⭐⭐ (Perfect) / ⭐⭐⭐ (Good) / ⭐⭐ (Poor)
- **Memory Persistence**: ⭐⭐⭐⭐⭐ (Perfect) / ⭐⭐⭐ (Good) / ⭐⭐ (Poor)

## 🔧 Improvement Recommendations

### 1. Profile Update Issues
**Problem**: Creating multiple profiles instead of updating existing one
**Solution**: 
- Fix profile merge logic in LangGraph nodes
- Implement proper profile update mechanism
- Add profile deduplication logic

### 2. Instruction Application
**Problem**: User instructions not being applied to new todos
**Solution**:
- Improve instruction recognition in prompts
- Ensure instructions are retrieved and applied during todo creation
- Add instruction validation in todo creation process

### 3. Priority and Deadline Setting
**Problem**: Priority levels and deadlines not being set despite instructions
**Solution**:
- Enhance prompt templates to include priority/deadline extraction
- Improve todo creation logic to apply user preferences
- Add validation for required fields

### 4. Data Quality Issues
**Problem**: Encoding issues and empty solution arrays
**Solution**:
- Fix text encoding in solution extraction
- Improve solution generation logic
- Add data validation and cleaning

### 5. Memory Consolidation
**Problem**: Multiple memory entries for same user
**Solution**:
- Implement memory consolidation logic
- Add memory deduplication
- Improve memory update vs. create logic

## 🎯 Testing Best Practices

### 1. Systematic Testing
- Always check memory state after each message
- Use consistent user IDs for testing
- Document expected vs. actual results

### 2. Performance Monitoring
- Track response times for each message
- Monitor memory usage and growth
- Check for memory leaks or data corruption

### 3. Data Quality Validation
- Verify data completeness and accuracy
- Check for encoding issues
- Validate data structure consistency

### 4. Edge Case Testing
- Test with empty messages
- Test with malformed JSON
- Test with very long messages
- Test concurrent user sessions

## 📈 Expected Performance Benchmarks

### Response Times:
- **Simple messages**: < 1 second
- **Complex messages**: < 2 seconds
- **Memory retrieval**: < 0.5 seconds

### Memory Accuracy:
- **Profile updates**: 90%+ success rate
- **Todo creation**: 95%+ success rate
- **Instruction application**: 80%+ success rate

### Data Quality:
- **Complete todos**: 90%+ with all fields populated
- **Valid priorities**: 80%+ when instructions provided
- **Proper deadlines**: 70%+ when deadlines mentioned

## 🎯 Success Criteria

### Basic Functionality:
- ✅ Server starts without errors
- ✅ All endpoints respond correctly
- ✅ Health check returns "healthy"
- ✅ Chat endpoint processes messages
- ✅ Memory CRUD operations work
- ✅ Error handling works properly
- ✅ API documentation is accessible
- ✅ Response times are reasonable (< 2s)

### Advanced Memory Testing:
- ✅ Profile creation and updates work correctly
- ✅ Todo creation with detailed information
- ✅ Instruction storage and application
- ✅ Memory persistence across sessions
- ✅ User isolation and data separation
- ✅ Memory consolidation (no duplicates)

## 🐛 Troubleshooting

### Server Issues:
**If server doesn't start:**
1. Check if port 8000 is available
2. Verify virtual environment is activated
3. Check for missing dependencies
4. Verify GOOGLE_API_KEY is set

### Memory Issues:
**If memory operations fail:**
1. Check GOOGLE_API_KEY is set
2. Verify LangGraph is working
3. Check logs for specific errors
4. Test with `/api/v1/memories/all/{user_id}` endpoint

### Performance Issues:
**If responses are slow:**
1. Check Google API quota and limits
2. Monitor container resource usage
3. Verify network connectivity
4. Check for memory leaks in logs

## 📊 Expected Results Summary

After successful testing, you should see:
- **Profile memories**: Stored and retrieved correctly
- **Todo items**: Created with detailed information and solutions
- **Instructions**: Learned and applied to new todos
- **Memory persistence**: Data survives across sessions
- **User isolation**: Each user maintains separate memory
- **Performance**: Fast response times and reliable operation
- **Data quality**: Complete, accurate, and well-structured data
