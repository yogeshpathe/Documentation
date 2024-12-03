
# Documentation for Frontend Developers: `/api/detect_object`

This endpoint enables object and text detection in an uploaded image using YOLO for object detection and EasyOCR for text recognition. Below is a detailed guide to integrate and use this endpoint in your frontend application.

---

## **Endpoint**
**POST** `/api/detect_object`

### **Description**
This endpoint processes an uploaded image to detect objects and text. It returns a JSON response containing the detected objects and any text found within the image.

---

## **Request Format**

### **Headers**
- `Content-Type: multipart/form-data`

### **Body Parameters**
| **Parameter** | **Type**      | **Description**               |
|---------------|---------------|--------------------------------|
| `file`        | `File` (image)| The image file to be analyzed. |

### **Supported File Formats**
- `JPEG`
- `PNG`
- `BMP`

---

## **Response Format**

### **Success (200 OK)**
The response will be a JSON object containing two main keys:
- **`objects`**: A list of detected object class names.
- **`texts`**: A list of detected text strings extracted from regions of interest.

#### Example Response
```json
{
  "objects": ["person", "car", "dog"],
  "texts": ["License Plate: ABC123", "Stop"]
}
```

### **Error (4xx or 5xx)**
If an error occurs, the response will contain an error message.

#### Example Error Response
```json
{
  "error": "An error occurred during object detection."
}
```

---

## **Frontend Integration Guide**

### **Steps to Use**
1. **Prepare the Image File**
   - Ensure the user uploads a valid image file.
   - Use an `<input type="file">` HTML element to capture the file.

2. **Send the File**
   - Use `FormData` in JavaScript to attach the image file to the request.

   #### Example Code (Using Fetch API)
   ```javascript
   const uploadImage = async (file) => {
       const formData = new FormData();
       formData.append("file", file);

       try {
           const response = await fetch("http://<your-backend-url>/api/detect_object", {
               method: "POST",
               body: formData,
           });

           if (!response.ok) {
               throw new Error("Failed to detect objects");
           }

           const data = await response.json();
           console.log("Detected Objects and Texts:", data);
       } catch (error) {
           console.error("Error:", error.message);
       }
   };

   // Example: Attach event listener to a file input
   document.getElementById("fileInput").addEventListener("change", (event) => {
       const file = event.target.files[0];
       if (file) {
           uploadImage(file);
       }
   });
   ```

3. **Handle the Response**
   - Display detected objects and texts in the UI.
   - For example, show objects as a list or overlay text annotations on the image.

---

## **Usage Notes**
- **Image Size**: Avoid uploading overly large images to ensure fast processing.
- **Display Results**: Highlight detected objects and texts visually for a better user experience.
  - Example: Draw bounding boxes for objects or overlay text on the detected regions.

---

## **Error Handling**
- Inform the user of errors gracefully (e.g., invalid file type or server error).
- Provide user-friendly feedback, such as "No objects detected" or "Unable to process the image."

---

## **Contact**
If you encounter any issues with the API, contact the backend development team for support.
