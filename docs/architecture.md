# Architecture Overview

Comprehensive architecture documentation for the Asis Memory Agent system.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Asis Memory Agent                        │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Server (Port 8000)                                │
│  ├── REST API Endpoints                                    │
│  ├── WebSocket Streaming                                   │
│  ├── Request Logging                                        │
│  └── Error Handling                                         │
├─────────────────────────────────────────────────────────────┤
│  LangGraph Core Engine                                      │
│  ├── State Management                                       │
│  ├── Node Processing                                        │
│  ├── Memory Operations                                      │
│  └── LLM Integration                                        │
├─────────────────────────────────────────────────────────────┤
│  Memory Storage (In-Memory)                                 │
│  ├── User Profiles                                          │
│  ├── Todo Items                                             │
│  └── Instructions                                           │
├─────────────────────────────────────────────────────────────┤
│  External Services                                          │
│  ├── Google Gemini API                                      │
│  └── Trustcall Extraction                                  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
MemA/
├── app/                       # FastAPI Application
│   ├── main.py               # FastAPI app entry point
│   ├── api/                  # API layer
│   │   ├── routes.py         # REST endpoints
│   │   ├── websocket.py      # WebSocket endpoints
│   │   └── dependencies.py   # Dependency injection
│   ├── models/               # Data models
│   │   └── requests.py       # Pydantic schemas
│   └── middleware/           # Middleware components
│       └── logging.py        # Request logging
├── graph/                    # LangGraph Core
│   ├── builder.py           # Graph construction
│   ├── nodes.py              # Processing nodes
│   ├── edges.py              # Flow control
│   └── state.py              # State definitions
├── chains/                   # LangChain Components
│   ├── prompts.py            # Prompt templates
│   └── extractors.py         # Data extraction
├── schemas/                  # Data Validation
│   ├── profile.py            # User profile schema
│   ├── todo.py               # Todo item schema
│   └── memory.py             # Memory schema
├── utils/                    # Utilities
│   ├── logging_config.py     # Logging setup
│   ├── metrics.py            # Performance metrics
│   └── helpers.py            # Helper functions
├── tests/                    # Test Suite
│   ├── test_agent.py         # Integration tests
│   ├── test_basic.py         # Unit tests
│   └── test_api.py           # API tests
└── docs/                     # Documentation
    ├── README.md             # Documentation index
    ├── quick-start.md        # Quick start guide
    ├── api-reference.md      # API documentation
    └── architecture.md       # This file
```

## 🔄 Data Flow

### 1. Request Processing Flow

```
Client Request
    ↓
FastAPI Router (Async Event Loop)
    ↓
Dependency Injection
    ↓
Request Validation (Pydantic)
    ↓
Executor Thread Pool
    ↓
LangGraph Processing (Sync in Thread Pool)
    ↓
Memory Operations (Singleton Store)
    ↓
LLM Generation
    ↓
Response Formatting
    ↓
Client Response
```

### Event Loop Strategy

The application uses a **hybrid async/sync approach** to handle FastAPI's async nature with LangGraph's synchronous API:

**Key Pattern**: FastAPI maintains async endpoints, while LangGraph's synchronous `invoke()` and `stream()` methods run in thread pool executors.

```
FastAPI Event Loop
├── Async Endpoint Handler
│   └── run_in_executor() → Thread Pool
│       └── graph.invoke() (Sync)
│           └── Memory Store (Shared Singleton)
│               └── InMemoryStore instance
└── Response to Client
```

**Benefits**:
- Non-blocking: FastAPI stays responsive during LLM processing
- Memory consistency: Singleton store instance shared across all threads
- No event loop conflicts: Sync code runs in separate threads
- Simple code: No need to convert entire LangGraph to async

**Implementation**:
- `app/api/routes.py`: Uses `loop.run_in_executor()` for `graph.invoke()`
- `app/api/websocket.py`: Uses `loop.run_in_executor()` for `graph.stream()`
- `graph/builder.py`: Creates singleton `InMemoryStore` instance
- All threads access the same store instance

### 2. Memory Management Flow

```
User Input
    ↓
Profile Extraction
    ↓
Todo Extraction
    ↓
Instruction Extraction
    ↓
Memory Storage
    ↓
Context Building
    ↓
LLM Processing
    ↓
Response Generation
```

## 🧩 Core Components

### FastAPI Server (`app/`)

**Purpose**: HTTP API interface and request handling

**Key Components**:
- **Main Application**: FastAPI app with CORS, middleware, and routing
- **REST Endpoints**: Async API that runs LangGraph sync methods in thread pool
- **WebSocket Endpoints**: Real-time streaming chat with executor pattern
- **Request Models**: Pydantic validation for all inputs/outputs
- **Middleware**: Logging, error handling, and request tracking

**Responsibilities**:
- HTTP request/response handling (async)
- Thread pool management for blocking operations
- Input validation and sanitization
- Error handling and status codes
- Request logging and metrics
- CORS and security headers

**Event Loop Integration**:
- Async endpoints maintain FastAPI's event loop
- Blocking LangGraph calls run in `asyncio.run_in_executor()`
- Prevents event loop blocking while maintaining async benefits
- Singleton memory store accessed consistently across threads

### LangGraph Engine (`graph/`)

**Purpose**: Core AI processing and workflow management

**Key Components**:
- **Graph Builder**: Constructs the processing workflow
- **Nodes**: Individual processing steps (chat, memory updates)
- **Edges**: Conditional routing between nodes
- **State Management**: Maintains conversation state

**Responsibilities**:
- Workflow orchestration
- State management
- Memory operations
- LLM integration
- Tool calling and extraction

### Memory System (`schemas/` + `chains/`)

**Purpose**: Persistent memory storage and retrieval

**Key Components**:
- **Profile Schema**: User information and preferences
- **Todo Schema**: Task management with solutions
- **Memory Schema**: Instruction learning and adaptation
- **Extractors**: AI-powered data extraction from conversations

**Responsibilities**:
- Memory persistence
- Data extraction and validation
- Context building for LLM
- Learning from user interactions

### Utilities (`utils/`)

**Purpose**: Cross-cutting concerns and shared functionality

**Key Components**:
- **Logging**: Structured logging with request tracking
- **Metrics**: Performance monitoring and statistics
- **Helpers**: Common utility functions

**Responsibilities**:
- Logging and monitoring
- Performance metrics
- Error tracking
- Configuration management

## 🔌 Integration Points

### External Services

#### Google Gemini API
- **Purpose**: Large language model for conversation
- **Integration**: Via LangChain Google GenAI integration
- **Configuration**: API key in environment variables
- **Usage**: Text generation, tool calling, memory extraction

#### Trustcall Extraction
- **Purpose**: Structured data extraction from conversations
- **Integration**: Custom extractors for profile, todos, instructions
- **Configuration**: Built into the extraction chains
- **Usage**: Memory updates, data validation

### Internal Integrations

#### FastAPI ↔ LangGraph
- **Interface**: Direct function calls to graph nodes
- **Data Flow**: Request → Graph Processing → Response
- **State Management**: Session-based state persistence
- **Error Handling**: Graceful degradation and error propagation

#### LangGraph ↔ Memory
- **Interface**: Direct store operations
- **Data Flow**: Extract → Validate → Store → Retrieve
- **Persistence**: In-memory storage (Phase 1)
- **Future**: Redis/PostgreSQL integration (Phase 2/3)

## 🚀 Deployment Architecture

### Development Environment

```
Developer Machine
├── Python Virtual Environment
├── FastAPI Development Server
├── In-Memory Storage
└── Local Testing
```

### Production Environment (Phase 1)

```
Docker Container
├── FastAPI Application
├── LangGraph Engine
├── In-Memory Storage
└── External API Calls
```

### Future Production Environment (Phase 2/3)

```
AWS ECS Fargate
├── FastAPI Application
├── LangGraph Engine
├── Redis Cache
├── PostgreSQL Database
└── External API Calls
```

## 📊 Performance Characteristics

### Response Times
- **Chat Endpoint**: ~0.6-0.9 seconds average
- **Memory Operations**: ~0.1-0.3 seconds
- **Health Check**: ~0.01 seconds
- **WebSocket Latency**: ~0.1-0.2 seconds

### Scalability
- **Concurrent Requests**: Limited by in-memory storage
- **Memory Usage**: ~50-100MB base + conversation data
- **CPU Usage**: Moderate during LLM processing
- **Network**: Minimal bandwidth requirements

### Limitations (Phase 1)
- **Memory Persistence**: Lost on server restart
- **Scalability**: Single instance only
- **Concurrency**: Limited by in-memory storage
- **Data Durability**: No persistence guarantees

## 🔒 Security Considerations

### Current Security (Phase 1)
- **Authentication**: None (public endpoints)
- **Authorization**: None (all users equal)
- **Data Encryption**: HTTPS recommended
- **Input Validation**: Pydantic validation
- **Error Handling**: Sanitized error messages

### Future Security (Phase 2/3)
- **Authentication**: JWT tokens or API keys
- **Authorization**: Role-based access control
- **Data Encryption**: At-rest and in-transit
- **Rate Limiting**: Per-user request limits
- **Audit Logging**: Comprehensive access logs

## 🔄 State Management

### Conversation State
- **Session ID**: Unique identifier per conversation
- **User ID**: Persistent user identification
- **Thread ID**: LangGraph conversation thread
- **Memory Context**: Retrieved memories for each request

### Memory State
- **Profile**: User information and preferences
- **Todos**: Task management and solutions
- **Instructions**: Learned behavioral patterns
- **Namespace**: Hierarchical memory organization

## 🧪 Testing Architecture

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **API Tests**: HTTP endpoint testing
- **Performance Tests**: Load and stress testing

### Test Data Management
- **Mock Services**: External API mocking
- **Test Fixtures**: Consistent test data
- **Isolation**: Independent test execution
- **Cleanup**: Automatic test data cleanup

## 🔮 Future Architecture (Phase 2/3)

### Phase 2: Redis Integration
```
FastAPI Server
├── Redis Cache
│   ├── Session Storage
│   ├── Response Caching
│   └── Rate Limiting
└── In-Memory Storage (Fallback)
```

### Phase 3: PostgreSQL Integration
```
FastAPI Server
├── Redis Cache (Session Layer)
├── PostgreSQL Database
│   ├── Persistent Memory Storage
│   ├── User Management
│   └── Analytics Data
└── External Services
```

This architecture provides a solid foundation for the memory agent while maintaining flexibility for future enhancements and scalability improvements.
