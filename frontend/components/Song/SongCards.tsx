"use client";
import React from "react";
import Song from "./Song";
import NotFound from "../NotFound/NotFound";
import axios from "axios";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { SongProps } from "./Song";

interface SongCardsProps {
  itemsPerPage: number;
  currentPage: number;
}

const SongCards: React.FC<SongCardsProps> = ({ itemsPerPage, currentPage }) => {
  const [data, setData] = useState<SongProps[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Reset loading state
      try {
        const response = await axios.get<SongProps[]>(
          `http://localhost:8000/dataset?page=${currentPage}`
        );
        // console.log("Data fetched:", response.data);
        alert(`length: ${response.data.length}`);
        setData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Failed to load dataset page ${currentPage + 1}`);
        handleTestClick();
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage]);

  const handleTestClick = () => {
    const placeholder = Array.from({ length: itemsPerPage }, (_, index) => ({
      fileName: `Lagu ${index + 1}`,
      mapping: {
        image: "/album/def.png",
        title: "Untitled",
        artist: "Anonymous",
      },
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
          {data.slice(0, 12).map((item, index) => (
            <div key={index} className="bg-[#608BC1]">
              <Song
                fileName={item.fileName}
                mapping={{
                  image: item.mapping?.image || "/album/def.png",
                  title: item.mapping?.title || "Untitled",
                  artist: item.mapping?.artist || "Anonymous",
                }}
              />
            </div>
          ))}
        </div>
      ) : (
        <div className="flex justify-center items-center h-full flex-col gap-3">
          <NotFound />
          <Button variant="outline" onClick={handleTestClick}>
            Click This to Test
          </Button>
        </div>
      )}
    </div>
  );  
};

export default SongCards;