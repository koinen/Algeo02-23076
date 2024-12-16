"use client";
import { useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { ButtonLoading } from "../Atom/Button";
import { useRouter } from "next/router"; // Import router

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
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = e.target.files?.[0];
    if (uploadedFile) {
      setFile(uploadedFile); // Save the file object

      // Only create a preview URL for image files
      if (text === "Image") {
        setImage(URL.createObjectURL(uploadedFile));
      } else {
        setImage(null); // No preview for non-image files
      }
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
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
        accept={
          text === "Song" ? ".mid" : text === "Mapping" ? ".json" : "image/*"
        } // Accept specific file types
        style={{ display: "none" }}
        onChange={handleFileChange}
      />
    </div>
  );
};

interface UploadProps {
  handleQuery: (data: any) => void;
  fetchData: () => void; // Add fetchData prop to reset data
}

const Upload: React.FC <UploadProps> = ({ handleQuery, fetchData }) => {
  const [image, setImage] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null); // Store file object for saving
  const [path, setPath] = useState<string>(""); // Store the current path
  const [loading, setLoading] = useState<boolean>(false); // Manage loading state

  // Handle Save button click
  const handleSave = async () => {
    if (!file) {
      alert("Please upload a file first.");
      return;
    }

    setLoading(true); // Set loading state to true

    // Use FormData to send file data to the server
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/upload_${path}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          validateStatus: () => true,
          timeout: 10000, // Allow all status codes to prevent unintentional rejection
        }
      );
      handleQuery(response.data);
      alert(`File uploaded successfully: ${response.data.path}`);
    } catch (error) {
      console.error("Error details:", error);
      alert(`Unexpected error occurred: ${error}`);
    } finally {
      setLoading(false); // Set loading state to false after the operation
    }
  };

  return (
    <div className="bg-[#133E87] mx-10 mt-5 rounded-xl p-5">
      <UploadButton
        text="Song"
        setImage={setImage}
        setFile={setFile}
        onClick={() => setPath("song")} // Set path for Song
      />
      <br />
      <UploadButton
        text="Image"
        setImage={setImage}
        setFile={setFile}
        onClick={() => setPath("image")} // Set path for Image
      />
      <br />
      <UploadButton
        text="Mapping"
        setImage={setImage}
        setFile={setFile}
        onClick={() => setPath("mapping")} // Set path for Mapping
      />
      {image && (
        <div
          style={{ marginTop: "20px" }}
          className="bg-[#F3F3E0] max-h-[20vh] overflow-scroll"
        >
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
      <br />
      <div className="flex justify-center items-center gap-6">
        {loading ? (
          <ButtonLoading />
        ) : (
          <Button variant="outline" onClick={handleSave} disabled={!file}>
            Save
          </Button>
        )}
        <Button
          variant="outline"
          onClick={() => {
            setImage(null);
            setFile(null);
            setPath("");
            fetchData();
          }}
          disabled={!file}
        >
          Cancel
        </Button>
      </div>
    </div>
  );
};

export default Upload;
