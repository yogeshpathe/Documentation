# Image Captioning API Documentation

## Base URL

All API endpoints are hosted at:

```
https://identity.cxhope.ai/image_captioning/
```

---

## Endpoints

### 1. **Health Check Endpoint**

#### URL
```
/
```

#### Method
GET

#### Description
This endpoint is used to verify that the API server is up and running.

#### Response
| Field    | Type   | Description                |
|----------|--------|----------------------------|
| message  | string | Health status of the API. |

#### Example Request
```javascript
fetch("https://identity.cxhope.ai/image_captioning/")
  .then((response) => response.json())
  .then((data) => console.log(data));
```

#### Example Response
```json
{
  "message": "Caption API is running."
}
```

---

### 2. **Generate Caption Endpoint**

#### URL
```
/generate-caption
```

#### Method
POST

#### Description
This endpoint accepts an image and a prompt, then returns a generated caption for the image.

#### Request Body
- **Form Data**:
  | Field  | Type     | Required | Description                                  |
  |--------|----------|----------|----------------------------------------------|
  | prompt | string   | Yes      | A predefined prompt from the dropdown list. |
  | file   | File     | Yes      | An image file (JPEG/PNG).                   |

#### Response
| Field           | Type   | Description                             |
|------------------|--------|-----------------------------------------|
| prompt          | string | The prompt sent in the request.         |
| caption_raw     | string | The raw generated caption.              |
| caption_wrapped | string | The caption wrapped for readability.    |

#### Example Request (Using Fetch in Next.js)
```javascript
const formData = new FormData();
formData.append("prompt", "Describe the scene in the image.");
formData.append("file", selectedImageFile);

fetch("https://identity.cxhope.ai/image_captioning/generate-caption", {
  method: "POST",
  body: formData,
})
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  })
  .then((data) => console.log(data))
  .catch((error) => console.error("Error generating caption:", error));
```

#### Example Response
```json
{
  "prompt": "Describe the scene in the image.",
  "caption_raw": "A group of people sitting around a table in a meeting room.",
  "caption_wrapped": "A group of people sitting\naround a table in a meeting\nroom."
}
```

---

## Frontend Integration Notes

### Handling Prompts
1. **Predefined Prompts**:
   Use the following predefined prompts for the `prompt` field:
   - Describe the objects in the image.
   - What is happening in the image?
   - What is the person wearing?
   - Describe the scene in the image.
   - Is there a computer in the image?
   - What is the person doing and what is on the desk?
   - Is the person interacting with any objects?
   - What is the background of the scene?
   - Is the person sitting or standing?
   - Is there anything unusual in the image?
   - What kind of environment is this?
   - Describe the lighting in the image.

2. **Dropdown in Frontend**:
   Ensure that a dropdown menu is implemented for the frontend to select prompts.

### File Upload
- The `file` field should accept JPEG or PNG image files.
- Use a file input or a webcam capture for the image source.

### Error Handling
- Handle non-2xx status codes gracefully in the frontend.
- Display user-friendly error messages when:
  - The server returns an error.
  - The image or prompt is not provided.

### Example Workflow in Next.js
Here is an example of how the frontend might call the API:

1. **Dropdown Selection**: Allow users to select a prompt from the predefined list.
2. **Image Upload**: Use a file input or webcam component to capture/upload an image.
3. **API Call**: Send the selected prompt and image as `FormData` to the `/generate-caption` endpoint.
4. **Display Response**: Show the returned captions (raw and wrapped) to the user.

---

## Testing
Ensure the following scenarios are tested:
- Valid prompt and valid image.
- Missing prompt or missing image (should return appropriate error messages).
- Large image file uploads.
- Selection of each prompt to verify the backend response.

