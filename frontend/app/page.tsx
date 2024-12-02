"use client";
import SongCards from "../components/Song/SongCards";
import Pagination from "../components/Pagination/Pagination";
import Upload from "../components/Upload/Upload";
import { useState } from "react";

let totalItems = 36;
const ITEMS_PER_PAGE = 12;

export default function HomePage() {
  const [currentPage, setCurrentPage] = useState(0);

  return (
    <div className="flex w-full bg-[#F3F3E0]">
      <div className="w-[20%] h-[86.5vh] bg-[#608BC1] mt-3 ml-3">
        <div className="flex flex-col">
          <Upload></Upload>
          <div className="flex justify-center items-center ">
            <Pagination
              totalItems={totalItems}
              itemsPerPage={ITEMS_PER_PAGE}
              currentPage={currentPage}
              setCurrentPage={setCurrentPage}
            ></Pagination>
          </div>
          <span className="text-center bg-[#F3F3E0]">Current Page: {currentPage + 1}</span>
        </div>
      </div>
      <SongCards
        totalItems={totalItems}
        itemsPerPage={ITEMS_PER_PAGE}
        currentPage={currentPage}
      />
    </div>
  );
}
