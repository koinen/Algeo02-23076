"use client";
import { useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";

interface ButtonProps {
  setImage: (image: string | null) => void;
  setFile: (file: File | null) => void;
  text: string;
  onClick: () => void; // Add an onClick prop to handle button-specific actions
}

const UploadButton: React.FC<ButtonProps> = ({
  setImage,
  setFile,
  text,
  onClick,
}) => {
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile); // Save the file object
      setImage(URL.createObjectURL(uploadedFile)); // Create a preview URL
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <Button variant="outline" onClick={onClick}>
        <label
          htmlFor={`upload-button-${text}`}
          style={{ cursor: "pointer", padding: "0 10px" }}
        >
          {text}
        </label>
      </Button>
      <input
        id={`upload-button-${text}`}
        type="file"
        accept="image/*"
        style={{ display: "none" }}
        onChange={handleImageChange}
      />
    </div>
  );
};

const Upload: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null); // Store file object for saving
  const [path, setPath] = useState<string>(""); // Store the current path

  // Handle Save button click
  const handleSave = async () => {
    if (!file) {
      alert("Please upload an image first.");
      return;
    }

    // Use FormData to send file data to the server
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post<{ path: string }>(
        `http://127.0.0.1:8000/upload_${path}/`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      alert(`File uploaded successfully: ${response.data.path}`);
    } catch (error) {
      alert(`File ${path} failed to upload`);
      console.error(error);
    }
  };

  return (
    <div>
      <UploadButton
        text="Song"
        setImage={setImage}
        setFile={setFile}
        onClick={() => setPath("song")} // Set path for Song
      />
      <UploadButton
        text="Image"
        setImage={setImage}
        setFile={setFile}
        onClick={() => setPath("image")} // Set path for Image
      />
      {image && (
        <div style={{ marginTop: "20px" }}>
          <p>Preview:</p>
          <img
            src={image}
            alt="preview"
            style={{
              maxWidth: "100%",
              maxHeight: "500px",
              borderRadius: "10px",
            }}
          />
        </div>
      )}

      <div className="flex justify-center items-center">
        <Button
          variant="outline"
          onClick={handleSave}
          style={{ marginTop: "10px" }}
        >
          Save
        </Button>
      </div>
    </div>
  );
};

export default Upload;