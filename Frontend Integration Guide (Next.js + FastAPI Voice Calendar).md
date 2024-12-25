# Calendar Integration API Documentation

## Base URL
All API endpoints are prefixed with:
```
https://identity.cxhope.ai/calendar
```

---

## Authentication

### Generate OAuth Login URL
**Endpoint:**
```
GET /generate-auth-url
```

**Description:**
Generates a Google OAuth 2.0 login URL for the user to authenticate with Google Calendar.

**Query Parameters:**
| Name     | Type   | Description                     |
|----------|--------|---------------------------------|
| user_id  | String | Unique user identifier (e.g., email). |

**Response:**
- **200 OK**
  ```json
  {
    "auth_url": "<google_oauth_url>"
  }
  ```
- **Error**
  ```json
  {
    "error": "<error_message>"
  }
  ```

**Example:**
```
GET https://identity.cxhope.ai/calendar/generate-auth-url?user_id=alice@example.com
```

**Frontend Workflow:**
- Make a `GET` request with the `user_id`.
- Open the `auth_url` in a new tab to let the user log in.

---

## Voice Commands

### Upload and Process Audio
**Endpoint:**
```
POST /voice-command
```

**Description:**
Uploads a recorded audio file, transcribes it, and processes the user’s intent (e.g., create an event or list events).

**Form Data:**
| Name        | Type    | Description                                    |
|-------------|---------|------------------------------------------------|
| file        | File    | The audio file (WAV format recommended).       |
| session_id  | String  | Unique session identifier.                     |
| user_id     | String  | Unique user identifier (e.g., email).          |

**Response:**
- **200 OK**
  ```json
  {
    "transcribed_text": "<transcription>",
    "session_id": "<session_id>",
    "reply": "<assistant_response>",
    "done": false,
    "intent": "<recognized_intent>"
  }
  ```

- **Error**
  ```json
  {
    "message": "<error_message>"
  }
  ```

**Example:**
```
POST https://identity.cxhope.ai/calendar/voice-command
```
**Form Data Example:**
```json
{
  "file": "conversation.wav",
  "session_id": "session_1672505600",
  "user_id": "alice@example.com"
}
```

**Frontend Workflow:**
- Record the user’s audio.
- Send the audio file, `session_id`, and `user_id` to this endpoint.
- Handle the `transcribed_text` and `reply` fields to update the UI.

---

## Token Callback

### OAuth Callback
**Endpoint:**
```
GET /oauth2callback
```

**Description:**
Receives the OAuth code from Google after the user logs in and exchanges it for a token. This endpoint is called automatically by Google during the OAuth process.

**Query Parameters:**
| Name  | Type   | Description                              |
|-------|--------|------------------------------------------|
| code  | String | Authorization code returned by Google.    |
| state | String | User ID passed during `generate-auth-url`. |

**Response:**
- **200 OK**
  ```json
  {
    "message": "Authentication successful! Token generated.",
    "status": "success"
  }
  ```
- **Error**
  ```json
  {
    "error": "<error_message>"
  }
  ```

**Example:**
```
GET https://identity.cxhope.ai/calendar/oauth2callback?code=<code>&state=alice@example.com
```

**Frontend Workflow:**
- This endpoint is automatically called during the OAuth flow.

---

## Notes for Integration
1. **User ID:**
   - Ensure that the `user_id` (e.g., email) is passed consistently across requests.

2. **Session ID:**
   - Generate a unique `session_id` for every conversation session.

3. **CORS:**
   - Make sure your Next.js app is allowed in the CORS settings of the backend.

4. **Error Handling:**
   - Provide user-friendly messages for errors returned by the API.

---

## Example Workflow

1. **Login with Google:**
   - `GET /generate-auth-url?user_id=alice@example.com`
   - Redirect user to the returned `auth_url`.

2. **Record and Upload Audio:**
   - Record audio in the browser.
   - Send the audio file to `POST /voice-command` along with `session_id` and `user_id`.
   - Display the transcription and response from the API.

3. **Schedule Event or List Events:**
   - Handle intents (`create_event`, `list_events`, etc.) based on the API response.

---

For questions or support, contact the backend team at `support@cxhope.ai`.

