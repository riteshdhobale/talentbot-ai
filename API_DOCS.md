# TalentScout API Documentation

This document describes the REST API endpoints for integrating the TalentScout backend with your frontend.

## Base URL

```
http://localhost:8000
```

## Running the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python api.py

# Or with uvicorn directly
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

### 1. Create Session

Create a new conversation session.

**Endpoint:** `POST /api/sessions`

**Request Body:** None

**Response:**
```json
{
  "session_id": "uuid-string",
  "conversation_stage": "collection",
  "collected_fields": {},
  "missing_fields": [
    "full_name",
    "email",
    "phone",
    "years_experience",
    "desired_position",
    "current_location",
    "tech_stack"
  ],
  "chat_history": [
    {
      "role": "assistant",
      "content": "Hello! I'm TalentScout..."
    }
  ]
}
```

### 2. Get Session

Get current session information.

**Endpoint:** `GET /api/sessions/{session_id}`

**Response:** Same as Create Session

### 3. Send Message

Send a message to the chatbot and get a response.

**Endpoint:** `POST /api/message`

**Request Body:**
```json
{
  "session_id": "uuid-string",
  "message": "John Doe"
}
```

**Response:**
```json
{
  "response": "Thank you, John Doe! What's your email address?",
  "conversation_stage": "collection",
  "fields_collected": {
    "full_name": "John Doe"
  },
  "missing_fields": [
    "email",
    "phone",
    "years_experience",
    "desired_position",
    "current_location",
    "tech_stack"
  ],
  "questions": null
}
```

**When all fields are collected:**
```json
{
  "response": "Great! I have all the information...",
  "conversation_stage": "questions",
  "fields_collected": {
    "full_name": "John Doe",
    "email": "john@example.com",
    ...
  },
  "missing_fields": [],
  "questions": [
    {
      "text": "Explain the key differences between Python and another language...",
      "difficulty": 1,
      "difficulty_stars": "★"
    },
    ...
  ]
}
```

### 4. Generate Questions

Manually trigger question generation (optional).

**Endpoint:** `POST /api/generate-questions`

**Request Body:**
```json
{
  "session_id": "uuid-string"
}
```

**Response:**
```json
{
  "questions": [
    {
      "text": "Question text here",
      "difficulty": 2,
      "difficulty_stars": "★★"
    }
  ]
}
```

## Conversation Flow

1. **Create Session** → Get initial greeting
2. **Send Messages** → Collect fields one by one
3. **Monitor `missing_fields`** → Track progress
4. **When `missing_fields` is empty** → Questions are automatically generated
5. **Continue sending messages** → Answer questions or chat

## Field Names

- `full_name`: Full name of the candidate
- `email`: Email address
- `phone`: Phone number
- `years_experience`: Years of experience (number)
- `desired_position`: Desired position(s)
- `current_location`: Current location
- `tech_stack`: Array of technologies (e.g., `["Python", "Django", "PostgreSQL"]`)

## Conversation Stages

- `greeting`: Initial greeting (auto-handled)
- `collection`: Collecting candidate information
- `questions`: Asking/answering technical questions
- `exit`: Conversation ended

## Exit Keywords

The following keywords will trigger an exit: `exit`, `bye`, `quit`, `thank you`, `stop`

## Error Handling

All endpoints return standard HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message here"
}
```

## CORS

The API has CORS enabled for all origins. Configure this for production.

## Example Integration (JavaScript/TypeScript)

```javascript
// Create session
const sessionResponse = await fetch('http://localhost:8000/api/sessions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
});
const session = await sessionResponse.json();
const sessionId = session.session_id;

// Send message
const messageResponse = await fetch('http://localhost:8000/api/message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    message: 'John Doe'
  })
});
const response = await messageResponse.json();
console.log(response.response); // Bot's response
```

## Environment Variables

Make sure to set these in your `.env` file:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: `gpt-3.5-turbo`)
- `ENABLE_STORAGE`: Enable storage (default: `true`)

