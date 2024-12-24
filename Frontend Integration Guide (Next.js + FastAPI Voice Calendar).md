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
