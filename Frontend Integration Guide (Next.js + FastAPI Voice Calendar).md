# Frontend Integration Guide (Next.js + FastAPI Voice Calendar)

This guide explains how to **call our multi-turn voice conversation API** from a **Next.js** frontend. The API is provided by a **FastAPI** server that handles:

1. **Audio to Text** transcription (via `SpeechRecognition` and `pydub`).
2. **Stateful Conversation** (using a session-based approach).
3. **Google Calendar** event creation and listing.

---

## **Overview**

### **Key Endpoint**

- **`POST /api/voice-command`**  
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
  
### **Conversation Flow**

1. **Obtain / Generate a `session_id`.**  
   - Each user session must have its own `session_id`.  
   - You can generate a random UUID or any unique string on the client.  
   - Use **the same `session_id`** for all subsequent requests in this conversation.

2. **Send Audio to `/api/voice-command`**.  
   - The server **transcribes** the audio, **updates** the conversation state (e.g. asking for date, time, etc.), and returns a **reply**.

3. **Use the Response**.  
   - Display or speak `reply` to the user.  
   - If `"done": true`, the conversation flow is complete. If `false`, the user should continue speaking until the conversation is finished.

---

## **Sample Frontend Code (Next.js)**

Below is a **minimal** snippet illustrating how to:

1. **Record / Upload Audio** from the microphone.
2. **Send** the audio with a **`session_id`**.
3. **Handle** the server’s JSON response.

> **Important**: This snippet assumes you have a way to record or capture audio in the browser as a `Blob` or `File` object.

```jsx
// pages/test_conversation.js

import React, { useState } from 'react';

export default function TestConversation() {
  const [sessionId, setSessionId] = useState(() => {
    // Could generate a random string/UUID:
    return Math.random().toString(36).substring(7);
  });
  const [messages, setMessages] = useState([]);
  const [recordedBlob, setRecordedBlob] = useState(null); // e.g. from MediaRecorder
  const [loading, setLoading] = useState(false);

  const API_URL = 'http://localhost:8000/api/voice-command';

  // Example function to upload the audio blob
  async function sendAudioToServer() {
    if (!recordedBlob) {
      alert('No audio recorded!');
      return;
    }
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('session_id', sessionId);
      formData.append('file', recordedBlob, 'voice_input.wav');

      const res = await fetch(API_URL, {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status} ${res.statusText}`);
      }

      const json = await res.json();
      console.log('Server response:', json);

      // Update local message list
      setMessages((prev) => [
        ...prev,
        {
          user: 'You',
          text: '...audio message...',
        },
        {
          user: 'Assistant',
          text: json.reply,
          transcribedText: json.transcribed_text,
          done: json.done,
          intent: json.intent,
        },
      ]);

      // If conversation is done, optionally reset or handle accordingly
      if (json.done) {
        alert('Conversation finished!');
      }
    } catch (err) {
      console.error('Error:', err);
    } finally {
      setLoading(false);
      // Clear the recorded blob if you want to record again
      setRecordedBlob(null);
    }
  }

  return (
    <div style={{ margin: 20 }}>
      <h1>Multi-Turn Voice Conversation</h1>
      <p>Session ID: <b>{sessionId}</b></p>

      {/* 
        TODO: Add your own audio recording UI here.
        - For example, a Start/Stop button that uses MediaRecorder
        - When complete, store the resulting Blob in `recordedBlob`.
      */}

      <button onClick={sendAudioToServer} disabled={loading || !recordedBlob}>
        {loading ? 'Processing...' : 'Send Audio to Server'}
      </button>

      <div style={{ marginTop: 20 }}>
        <h2>Conversation Log</h2>
        <ul>
          {messages.map((m, idx) => (
            <li key={idx}>
              <strong>{m.user}:</strong> {m.text}
              {m.transcribedText && (
                <div style={{ fontStyle: 'italic', color: 'gray' }}>
                  (transcribed: {m.transcribedText})
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
