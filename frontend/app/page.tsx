"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";
import Pagination from "../components/Pagination/Pagination";
import SongCards from "../components/Song/SongCards";
import Upload from "../components/Upload/Upload";
import Humming from "@/components/Humming/Humming";

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
  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState<SongProps[]>([]);

  useEffect(() => {
    fetchData();
  }, [currentPage]); // Add currentPage to the dependency array

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch item count
      const countResponse = await axios.get("http://127.0.0.1:8000/count");
      // alert("item count :" + countResponse.data);
      setItemCount(countResponse.data);

      const dataResponse = await axios.get(
        `http://localhost:8000/dataset?page=${currentPage + 1}`
      );
      // alert("currentPage :" + (currentPage + 1));
      // alert("data length :" + dataResponse.data.length);
      setData(dataResponse.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      // alert("item count :" + itemCount);
      // alert("data length :" + data.length);
      setData([]);
      alert("Failed to load data. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async (data: SongProps[]) => {
    setData(data);
  };

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
            <Upload handleQuery={handleQuery} fetchData={fetchData} />
            <div className="flex justify-center items-center h-[15vh]">
              <Pagination
                totalItems={itemCount}
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
              />
            </div>
            <span className="text-center bg-[#F3F3E0]">
              Current Page: {currentPage + 1}
            </span>
            <br />
            <Humming handleQuery={handleQuery} fetchData={fetchData} />
          </div>
        </div>
        <SongCards data={data} currentPage={currentPage} />
      </div>
    </div>
  );
}
