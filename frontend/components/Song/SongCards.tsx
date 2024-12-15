"use client";
import React from "react";
import Song from "./Song";
import NotFound from "../NotFound/NotFound";
import axios from "axios";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import type { SongProps } from "./Song";

interface SongCardsProps {
  itemsPerPage: number;
  currentPage: number;
}

const SongCards: React.FC<SongCardsProps> = ({ itemsPerPage, currentPage }) => {
  const [data, setData] = useState<SongProps[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Ensure loading state resets when fetching new data
      try {
        const response = await axios.get(
          `http://localhost:8000/dataset?page=${currentPage}`
        );
        setData(response.data);
      } catch (error) {
        alert(`Failed to load dataset page ${currentPage + 1}`);
        handleTestClick();
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage]); // Add currentPage as a dependency

  const currentItems = data.slice(0, 12);

  const handleTestClick = () => {
    const placeholder = Array.from({ length: itemsPerPage }, (_, index) => ({
      fileName: `Lagu ${index + 1}`,
    }));
    setData(placeholder);
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="w-[80%] h-[86.5vh] p-3">
      {data.length > 0 ? (
        <div className="grid grid-cols-4 grid-rows-3 gap-3">
          {currentItems.map((item, index) => (
            <div key={index} className="bg-[#608BC1]">
              <Song
                fileName={item.fileName || "not found"}
                mapping={
                  item.mapping || {
                    imageAbsolutePath: "/album/def.png",
                    title: "Untitled",
                    artist: "Anonymous",
                  }
                }
              />
            </div>
          ))}
        </div>
      ) : (
        <div className="flex justify-center items-center h-full">
          <NotFound></NotFound>
          <Button variant="outline" onClick={handleTestClick}>
            Click This to Test
          </Button>
        </div>
      )}
    </div>
  );
};

export default SongCards;
