# Frontend Integration Guide (Next.js + FastAPI Voice Calendar)

This guide explains how to integrate the **FastAPI Voice Calendar API** with a **Next.js** frontend.

---

## **Overview**

### **Key Endpoint**

- **`POST /calendar/voice-command`**  
  - **Expects**: 
    - **Multipart/form-data** with:
      1. `file` (the audio blob from browser)
      2. `session_id` (a string that identifies the user’s conversation)
  - **Returns**: JSON object with:
    ```json
    {
      "transcribed_text": "...",
      "session_id": "...",
      "reply": "...",
      "done": false,
      "intent": "create_event"
    }
    ```

---

## **Conversation Flow**

1. **Generate a `session_id`**  
   - Each conversation must have a unique `session_id`.
   - Use **the same `session_id`** for all requests in this conversation.

2. **Send Audio to `/calendar/voice-command`**  
   - The server transcribes the audio, updates the conversation state, and returns a reply.

3. **Handle the Response**  
   - Display or use the `reply` text to guide the user.  
   - If `"done": true`, the conversation is complete.

---

## **API Integration Steps**

### **Request Format**

- **Method**: `POST`
- **URL**: `/calendar/voice-command`
- **Headers**:
  - `Content-Type: multipart/form-data`
- **Body**:
  - `session_id`: Unique string identifier for the session (e.g., UUID or random string).
  - `file`: Audio file (`Blob` or `File` object from the browser).

### **Response Format**

```json
{
  "transcribed_text": "Your speech as text",
  "session_id": "The same session_id",
  "reply": "Assistant's response",
  "done": false,
  "intent": "create_event"
}

```



# Example Frontend Code

This section provides a Next.js frontend implementation for interacting with the `/calendar/voice-command` API. The code demonstrates:

1. **Session Management**: A unique `session_id` is generated for each conversation.
2. **Audio Recording**: A placeholder for audio recording logic.
3. **API Communication**: Sending the recorded audio and session details to the backend.
4. **Conversation Flow**: Displaying the assistant's replies and tracking the conversation state.

---

## **Next.js Frontend Example**

Below is a complete example of a **React component** in a Next.js application.

```jsx
import React, { useState } from 'react';

export default function VoiceCalendar() {
  const [sessionId, setSessionId] = useState(() => {
    // Generate a random session ID
    return Math.random().toString(36).substring(2);
  });
  const [messages, setMessages] = useState([]);
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:8000/calendar/voice-command';

  // Function to send audio to the server
  async function sendAudioToServer() {
    if (!recordedBlob) {
      alert('Please record some audio first!');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('file', recordedBlob, 'voice_input.wav');

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Server response:', data);

      // Update messages
      setMessages((prev) => [
        ...prev,
        { user: 'You', text: '...audio message...' },
        { user: 'Assistant', text: data.reply },
      ]);

      if (data.done) {
        alert('Conversation finished!');
      }
    } catch (err) {
      console.error('Error:', err);
      alert('An error occurred while communicating with the server.');
    } finally {
      setLoading(false);
      setRecordedBlob(null); // Clear the audio for next input
    }
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Voice Calendar</h1>
      <p>Session ID: <b>{sessionId}</b></p>

      {/* Add your audio recording UI here */}
      {/* Assume setRecordedBlob updates with the recorded audio blob */}

      <button onClick={sendAudioToServer} disabled={!recordedBlob || loading}>
        {loading ? 'Processing...' : 'Send Audio'}
      </button>

      <div style={{ marginTop: 20 }}>
        <h2>Conversation Log</h2>
        <ul>
          {messages.map((msg, idx) => (
            <li key={idx}><strong>{msg.user}:</strong> {msg.text}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

