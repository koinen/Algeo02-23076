"use client";
import React from "react";
import Song from "./Song";
import NotFound from "../NotFound/NotFound";
import { Button } from "@/components/ui/button";
import { SongProps } from "./Song";

interface SongCardsProps {
  data: SongProps[];
}

const SongCards: React.FC<SongCardsProps> = ({ data }) => {
  // const [data, setData] = useState<SongProps[]>([]);
  // const [loading, setLoading] = useState<boolean>(true);

  // useEffect(() => {
  //   const fetchData = async () => {
  //     setLoading(true); // Reset loading state
  //     try {
  //       // alert(`Fetching dataset page ${currentPage + 1}`);
  //       const response = await axios.get(
  //         `http://localhost:8000/dataset?page=${currentPage + 1}`
  //       );
  //       // console.log("Data fetched:", response.data);
  //       // alert(`length: ${response.data.length}`);
  //       setData(response.data);
  //     } catch (error) {
  //       console.error("Error fetching data:", error);
  //       alert(`Failed to load dataset page ${currentPage + 1}`);
  //       handleTestClick();
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchData();
  // }, [currentPage]);

  // const handleTestClick = () => {
  //   const placeholder = Array.from({ length: itemsPerPage }, (_, index) => ({
  //     fileName: `Lagu ${index + 1}`,
  //     mapping: {
  //       image: "def.png",
  //       title: "Untitled",
  //       artist: "Anonymous",
  //     },
  //   }));
  //   setData(placeholder);
  // };


  return (
    <div className="w-[80%] h-[86.5vh] p-3 overflow-y-auto">
      {data.length > 0 ? (
        <div className="grid grid-cols-4 grid-rows-3 gap-3">
          {data.slice(0, 12).map((item, index) => (
            <div key={index} className="bg-[#608BC1]">
              <Song
                song={item}
                index={index}
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