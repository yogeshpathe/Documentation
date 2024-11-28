# Emotion Detection API Documentation

## Overview

This API detects emotions from an uploaded image and returns the most probable emotions for each detected face. It uses [DeepFace](https://github.com/serengil/deepface) for emotion analysis and is optimized to always return results as an array.

## Endpoint

### `POST /api/detect_emotion`

This endpoint takes an uploaded image file and returns the emotions detected in the faces present in the image.

## Request Format

- **URL**: `/api/detect_emotion`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: The image file to analyze. The file must be uploaded as `multipart/form-data` using the field name `file`.

### Example Request

```bash
curl -X POST "http://<server-url>/api/detect_emotion" -F "file=@path/to/your/image.jpg"
```

## Response Format

- **Content-Type**: `application/json`
- **Fields**:
  - `message`: A summary message about the number of people detected.
  - `results`: An array containing details about each detected face, including emotions and bounding boxes.

### Response Structure

- **`message`** (string): A summary message with the count of detected faces.
- **`results`** (array): List of detected persons with the following attributes:
  - **`person`** (integer): The detected person number (1-indexed).
  - **`emotion`** (string): The dominant emotion detected for the person.
  - **`confidence`** (float): The confidence score for the detected emotion (0.0 - 1.0).
  - **`bounding_box`** (object): Contains the bounding box information for the detected face with keys: `x`, `y`, `w`, and `h`.

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

## Notes for Frontend Integration

- Ensure that the `file` parameter is included as `multipart/form-data`.
- The response always contains a `results` array, which will be empty if no faces are detected.
- Prioritize the `message` field to handle user notifications appropriately based on the detection outcome.

### Response Considerations
- When parsing the response, always iterate over the `results` array to extract information about detected faces.
- The emotion detection may prioritize "surprise" if its confidence exceeds the configured threshold (`0.6`). Adjust user interface messaging accordingly if this is a significant factor.

## Logging

This API logs the following:
- Requests made to the `/api/detect_emotion` endpoint.
- Status of image reading and completion of emotion detection.
- Errors, if any occur during the detection process.

