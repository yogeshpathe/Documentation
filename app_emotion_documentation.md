# Emotion Detection API Documentation

## Overview

The Emotion Detection API detects emotions from an uploaded image and returns the most probable emotions for each detected face. It utilizes [DeepFace](https://github.com/serengil/deepface) for emotion analysis and is optimized to always return results as an array. This documentation provides details on how to integrate and use this API effectively.

## Endpoint

### `POST /api/detect_emotion`

This endpoint accepts an uploaded image file and returns the detected emotions for each face present in the image.

## Request Format

- **URL**: `/api/detect_emotion`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): The image file to analyze. The file must be uploaded as `multipart/form-data` using the field name `file`.

### Example Request

```bash
curl -X POST "https://identity.cxhope.ai/api/detect_emotion" -F "file=@path/to/your/image.jpg"
```

## Response Format

- **Content-Type**: `application/json`
- **Fields**:
  - `message` (string): A summary message about the number of people detected.
  - `results` (array): An array containing details about each detected face, including emotions and bounding boxes.

### Response Structure

- **`message`** (string): A summary message indicating the number of detected faces.
- **`results`** (array): List of detected persons with the following attributes:
  - **`person`** (integer): The index of the detected person (starting from 1).
  - **`emotion`** (string): The dominant emotion detected for the person.
  - **`confidence`** (float): The confidence score for the detected emotion (0.0 - 1.0).
  - **`bounding_box`** (object): Contains the bounding box information for the detected face, with keys: `x`, `y`, `w`, and `h`.

### Example Response

```json
{
  "message": "1 person detected.",
  "results": [
    {
      "person": 1,
      "emotion": "happy",
      "confidence": 0.98,
      "bounding_box": {
        "x": 100,
        "y": 150,
        "w": 50,
        "h": 60
      }
    }
  ]
}
```

## Error Handling

- If no faces are detected in the uploaded image, the response will look like:
  ```json
  {
    "message": "No faces detected.",
    "results": []
  }
  ```
- If there is an internal error during processing, the response will include an `error` field:
  ```json
  {
    "error": "An error occurred during emotion detection."
  }
  ```

## Integration Notes for Frontend Developers

- Ensure that the `file` parameter is included as `multipart/form-data` when making requests.
- The response always contains a `results` array, which may be empty if no faces are detected.
- Use the `message` field to handle user notifications appropriately based on the detection outcome.

### Response Considerations

- Always iterate over the `results` array to extract information about detected faces.
- The emotion detection may prioritize "surprise" if its confidence exceeds a configured threshold (`0.6`). Adjust user interface messaging accordingly if this is a significant factor.
- Each detected face is assigned an index starting from `1`, allowing easy identification of multiple faces.

## Logging Details

This API maintains logs for the following activities:

- Requests made to the `/api/detect_emotion` endpoint.
- Status of image reading and the completion of emotion detection.
- Errors encountered during the detection process, with descriptive messages for easier debugging.

## Best Practices

- Use high-quality images with clear visibility of faces for better accuracy in emotion detection.
- Avoid using images with heavy shadows, occlusions, or blurriness, as they may affect the detection results.

## Example Frontend Integration

Here's an example of how to integrate the API with JavaScript using `fetch`:

```javascript
const formData = new FormData();
formData.append('file', imageFile);

fetch('http://<server-url>/api/detect_emotion', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log(data.message);
    data.results.forEach(person => {
      console.log(`Person ${person.person}: Emotion - ${person.emotion}, Confidence - ${person.confidence}`);
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

This example demonstrates how to create a `FormData` object, append the image file, and send it to the API. The response is then processed to extract information about detected faces.

