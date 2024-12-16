"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import Pagination from "../components/Pagination/Pagination";
import SongCards from "../components/Song/SongCards";
import Upload from "../components/Upload/Upload";
import Humming from "@/components/Humming/Humming";

const ITEMS_PER_PAGE = 12;

interface SongProps {
  fileName: string;
  mapping: {
    image?: string;
    title?: string;
    artist?: string;
  };
}

export default function HomePage() {
  const [currentPage, setCurrentPage] = useState(0);
  const [itemCount, setItemCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<SongProps[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch item count
        const countResponse = await axios.get("http://127.0.0.1:8000/count/");
        setItemCount(countResponse.data);

        // Fetch data for the current page
        const dataResponse = await axios.get(
          `http://localhost:8000/dataset?page=${currentPage + 1}`
        );
        setData(dataResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to load data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage]); // Add currentPage to the dependency array

  if (loading) {
    return <div>Loading...</div>;
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
            <div className="flex justify-center items-center h-[15vh]">
              <Pagination
                totalItems={itemCount}
                itemsPerPage={ITEMS_PER_PAGE}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
              />
            </div>
            <span className="text-center bg-[#F3F3E0]">
              Current Page: {currentPage + 1}
            </span>
            <br />
            <Humming />
          </div>
        </div>
        <SongCards
          itemsPerPage={ITEMS_PER_PAGE}
          currentPage={currentPage}
          data={data}
        />
      </div>
    </div>
  );
}