"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Pagination from "../components/Pagination/Pagination";
import SongCards from "../components/Song/SongCards";
import Upload from "../components/Upload/Upload";
import { Button } from "@/components/ui/button";

interface SongItem {
  title: string;
  image?: string;
}

const ITEMS_PER_PAGE = 12;

export default function HomePage() {
  const [currentPage, setCurrentPage] = useState(0);
  const [data, setData] = useState<SongItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/dataset/");
        setData(response.data);
      } catch (error) {
        alert("Failed to load dataset");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleTestClick = () => {
    const placeholder = Array.from({ length: 50 }, (_, index) => ({
      title: `foto ${index + 1}`,
    }));
    setData(placeholder);
  };

  const totalItems = data.length;

  if (loading) {
    return (
      <div className="bg-[#608BC1] flex justify-center items-center h-screen">
        Loading...
      </div>
    );
  }

  return (
    <div
      className="flex flex-col justify-center items-center h-screen bg-[#608BC1]"
      suppressHydrationWarning
    >
      <div className="flex h-full w-full">
        <div className="w-[20%] bg-[#608BC1]">
          <div className="flex flex-col">
            <Upload />
            <div className="flex justify-center items-center">
              <Pagination
                totalItems={totalItems}
                itemsPerPage={ITEMS_PER_PAGE}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
              />
            </div>
            <span className="text-center bg-[#F3F3E0]">
              Current Page: {currentPage + 1}
            </span>
            <br />
            <Button variant="outline" onClick={handleTestClick}>
              Click This to Test
            </Button>
          </div>
        </div>
        <SongCards
          data={data}
          itemsPerPage={ITEMS_PER_PAGE}
          currentPage={currentPage}
        />
      </div>
    </div>
  );
}
