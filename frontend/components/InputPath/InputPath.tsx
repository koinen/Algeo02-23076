"use client"
import React, { useState } from "react";
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

export function InputPath() {
  const [path, setPath] = useState<string>("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/upload_dataset/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ path }),
      });

      if (response.ok) {
        alert("Dataset path submitted successfully!");
      } else {
        const errorData = await response.json();
        alert(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error("Error submitting dataset path:", error);
      alert("Failed to submit the dataset path.");
    }
  };

  return (
    <Card className="w-[50%] h-[50vh] bg-gray-200">
      <CardHeader>
        <CardTitle>
          <p className="text-6xl">Set Your Data Set</p>
        </CardTitle>
        <CardDescription>Enter the absolute path to your folder</CardDescription>
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
            <Button variant="outline" type="button">
              Cancel
            </Button>
            <Button type="submit">Submit</Button>
          </CardFooter>
        </form>
      </CardContent>
    </Card>
  );
}
