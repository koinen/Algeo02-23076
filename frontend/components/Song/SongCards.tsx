import React from 'react';
import Song from './Song';
import NotFound from '../NotFound/NotFound';

interface SongItem {
  title: string;
  image?: string;
}

interface SongCardsProps {
  data: SongItem[];
  itemsPerPage: number;
  currentPage: number;
}

const SongCards: React.FC<SongCardsProps> = ({ data, itemsPerPage, currentPage }) => {
  const startIndex = currentPage * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentItems = data.slice(startIndex, endIndex);

  return (
    <div className="w-[80%] h-[86.5vh] p-3">
      {data.length > 0 ? (
        <div className="grid grid-cols-4 grid-rows-3 gap-3">
          {currentItems.map((item, index) => (
            <div key={index} className="bg-[#608BC1]">
              <Song title={item.title || "not found"} image={item.image || "def.png"} />
            </div>
          ))}
        </div>
      ) : (
        <div className="flex justify-center items-center h-full">
          <NotFound></NotFound>
        </div>
      )}
    </div>
  );
};

export default SongCards;