"use client";
import React from "react";
import Song from "./Song";
import NotFound from "../NotFound/NotFound";
import { SongProps } from "./Song";

interface SongCardsProps {
  data: SongProps[];
  currentPage: number;
}

const SongCards: React.FC<SongCardsProps> = ({ data, currentPage }) => {

  return (
    <div className="w-[80%] h-[86.5vh] p-3 overflow-y-auto">
      {data.length > 0 ? (
        <div className="grid grid-cols-4 grid-rows-3 gap-3">
          {data.slice(0, 12).map((item, index) => (
            <div key={index} className="bg-[#608BC1]">
              <Song
                song={item}
                index={currentPage * 12 + index}
              />
            </div>
          ))}
        </div>
      ) : (
        <div className="flex justify-center items-center h-full flex-col gap-3">
          <NotFound />
        </div>
      )}
    </div>
  );  
};

export default SongCards;