import React, { useState, useRef } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { ButtonLoading } from "../Atom/Button";

const Humming: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState<string | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [loading, setLoading] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };
    mediaRecorderRef.current.onstop = () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioURL(audioUrl);
      setAudioBlob(audioBlob);
      audioChunksRef.current = [];
    };
    mediaRecorderRef.current.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const submitRecording = async () => {
    if (!audioBlob) {
      alert("No audio to submit");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", audioBlob, "humming.wav");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload_humming/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      alert(`File uploaded successfully: ${response.data.path}`);
    } catch (error) {
      alert("Failed to upload file humming");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col justify-center items-center mt-5">
      <Button
        variant="outline"
        onClick={isRecording ? stopRecording : startRecording}
      >
        {isRecording ? "Stop" : "Humming"}
      </Button>
      <br />
      {audioURL && (
        <div>
          <audio src={audioURL} controls />
          <br />
        </div>
      )}
      {loading ? (
        <ButtonLoading />
      ) : (
        <Button
          variant="outline"
          onClick={submitRecording}
          disabled={!audioBlob}
        >
          Search
        </Button>
      )}
    </div>
  );
};

export default Humming;
