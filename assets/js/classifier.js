import { MAX_FILE_SIZE_BYTES, SUPPORTED_MIME_TYPES } from "./constants.js";

export function validateImageFile(file) {
  if (!file) {
    return {
      valid: false,
      message: "Please upload an image to continue.",
    };
  }

  if (!SUPPORTED_MIME_TYPES.includes(file.type)) {
    return {
      valid: false,
      message: "Unsupported format. Please use JPG, PNG, or WEBP images only.",
    };
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    return {
      valid: false,
      message: "Image is too large. Maximum allowed size is 10MB.",
    };
  }

  return {
    valid: true,
    message: "",
  };
}

export function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (event) => resolve(event.target.result);
    reader.onerror = () => reject(new Error("Could not read image file."));

    reader.readAsDataURL(file);
  });
}
