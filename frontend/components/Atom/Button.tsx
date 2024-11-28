"use client";

import { Button } from "@/components/ui/button";
import { useState } from "react";
import axios from "axios";

interface ButtonProps {
  text: string;
}

const ButtonLight: React.FC<ButtonProps> = ({ text }) => {
    return (
        <Button variant="outline">
            <p className="p-7">{text}</p>
        </Button>
    );
}

const ImageUploadButton: React.FC<ButtonProps> = ({ text }) => {
    const [image, setImage] = useState<string | null>(null);
    const [file, setFile] = useState<File | null>(null); // Store file object for saving

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const uploadedFile = e.target.files?.[0];
        if (uploadedFile) {
        setFile(uploadedFile); // Save the file object
        setImage(URL.createObjectURL(uploadedFile)); // Create a preview URL
        }
    };

    const handleSave = async () => {
        if (!file) {
        alert("Please upload an image first.");
        return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
        const response = await axios.post("http://127.0.0.1:8000/upload/", formData, {
            headers: {
            "Content-Type": "multipart/form-data",
            },
        });
        alert(response.data.message);
        } catch (error) {
        alert("Failed to save the image. Try again.");
        console.error(error);
        }
    };

    return (
        <div style={{ textAlign: "center", marginTop: "20px" }}>
        <Button variant="outline">
            <label
            htmlFor="upload-button"
            style={{ cursor: "pointer", padding: "0 10px" }}
            >
            {text}
            </label>
        </Button>
        <input
            id="upload-button"
            type="file"
            accept="image/*"
            style={{ display: "none" }}
            onChange={handleImageChange}
        />

        {image && (
            <div style={{ marginTop: "20px" }}>
            <p>Preview:</p>
            <img
                src={image}
                alt="Uploaded preview"
                style={{ maxWidth: "100%", maxHeight: "300px", borderRadius: "10px" }}
            />
            <Button variant="outline" onClick={handleSave} style={{ marginTop: "10px" }}>
                Save
            </Button>
            </div>
        )}
        </div>
    );
};

export { ButtonLight, ImageUploadButton };