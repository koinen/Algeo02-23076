"use client";
import React, { useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ButtonLoading } from "../Atom/Button";

const InputPath: React.FC = () => {
  const [path, setPath] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!path) {
      alert("Please enter a path.");
      return;
    }

    setLoading(true); // Set loading state to true

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload_dataset/",
        { path }
      );
      alert(`Path submitted successfully: ${response.data.message}`);
    } catch (error) {
      alert(`Failed to submit path : ${path}`);
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-[50%] h-[50vh] mb-40 bg-gray-200">
      <CardHeader>
        <CardTitle>
          <p className="text-6xl">Set Your Data Set</p>
        </CardTitle>
        <CardDescription>
          Enter the absolute path to your folder
        </CardDescription>
      </CardHeader>
      <CardContent className="h-[60%]">
        <form onSubmit={handleSubmit}>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <label htmlFor="path">Absolute PATH</label>
              <Input
                id="path"
                placeholder="Enter PATH to your data set here"
                value={path}
                onChange={(e) => setPath(e.target.value)}
              />
            </div>
          </div>
          <CardFooter className="flex justify-between mt-[20vh]">
            <Button
              variant="outline"
              type="button"
              disabled={!path}
              onClick={() => setPath("")}
            >
              Cancel
            </Button>
            {loading ? (
              <ButtonLoading />
            ) : (
              <Button variant="outline" type="submit" disabled={!path}>
                Submit
              </Button>
            )}
          </CardFooter>
        </form>
      </CardContent>
    </Card>
  );
};

export default InputPath;
