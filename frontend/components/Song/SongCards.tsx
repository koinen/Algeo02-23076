import React from 'react';
import Song from './Song';

interface SongCardsProps {
  totalItems: number;
  itemsPerPage: number;
  currentPage: number;
}

const SongCards: React.FC<SongCardsProps> = ({ totalItems, itemsPerPage, currentPage }) => {
  const startIndex = currentPage * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentItems = Array.from({ length: totalItems }).slice(startIndex, endIndex);

  return (
    <div className="w-[80%] h-[86.5vh] p-3">
      <div className="grid grid-cols-4 grid-rows-3 gap-3">
        {currentItems.map((_, index) => (
          <div key={index} className="bg-[#608BC1]">
            <Song title={`Song ${startIndex + index + 1}`} image="def.png" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default SongCards;