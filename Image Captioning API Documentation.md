# Image Captioning API Documentation

This documentation provides guidance for the frontend team to interact with the Image Captioning API. The API has two primary endpoints:

- **Base URL:** `https://identity.cxhope.ai/image_captioning/`

## API Endpoints

### 1. Health Check Endpoint
**URL:** `/`

**Method:** `GET`

This endpoint is used to check if the API is running and healthy.

#### Example Request
```bash
GET https://identity.cxhope.ai/image_captioning/
```

#### Example Response
```json
{
  "message": "Caption API is running."
}
```

---

### 2. Generate Caption Endpoint
**URL:** `/generate-caption`

**Method:** `POST`

This endpoint processes an uploaded image and a user-selected prompt to generate a caption.

#### Request Headers
Ensure the request includes the correct headers:
- `Content-Type: multipart/form-data`

#### Request Parameters
The request must include:
- **`prompt`** (string): The selected prompt for image captioning. Use one of the predefined prompts listed below.
- **`file`** (file): The image file to be analyzed. The file must be in `jpeg`, `png`, or similar image formats.

#### Predefined Prompts
Frontend must present these options in a dropdown menu:
1. Describe the objects in the image.
2. What is happening in the image?
3. What is the person wearing?
4. Describe the scene in the image.
5. Is there a computer in the image?
6. What is the person doing and what is on the desk?
7. Is the person interacting with any objects?
8. What is the background of the scene?
9. Is the person sitting or standing?
10. Is there anything unusual in the image?
11. What kind of environment is this?
12. Describe the lighting in the image.

#### Example Request
```bash
POST https://identity.cxhope.ai/image_captioning/generate-caption
```

**Body (multipart/form-data):**
- `prompt`: "What is happening in the image?"
- `file`: [Upload an image file]

#### Example cURL Command
```bash
curl -X POST \
  https://identity.cxhope.ai/image_captioning/generate-caption \
  -H "Content-Type: multipart/form-data" \
  -F "prompt=What is happening in the image?" \
  -F "file=@/path/to/image.jpg"
```

#### Example Response
```json
{
  "prompt": "What is happening in the image?",
  "caption_raw": "A person is typing on a laptop in a dimly lit room.",
  "caption_wrapped": "A person is typing on a laptop\nin a dimly lit room."
}
```

---

## Notes for Frontend Team

1. **Dropdown Integration**:
   - Use the predefined list of prompts in the dropdown UI to ensure correct API usage.
   - Send the selected prompt as the `prompt` field in the POST request.

2. **Error Handling**:
   - Ensure proper handling of errors such as:
     - Missing `file` or `prompt` field.
     - Invalid image formats.
     - API connectivity issues.
   - Display meaningful error messages to users.

3. **Loading State**:
   - Implement a loading state while waiting for the API response.

4. **Image Upload Restrictions**:
   - Restrict file uploads to valid image formats (e.g., `jpeg`, `png`).
   - Limit file sizes if necessary to avoid timeouts.

5. **API Base URL**:
   - Use the provided base URL: `https://identity.cxhope.ai/image_captioning/`.

---

## Contact
For questions or issues, reach out to the backend team for support.
