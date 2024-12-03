import Song from "../components/Song/Song";
import Pagination from "../components/Pagination/Pagination";
import Upload from "../components/Upload/Upload";
export default function HomePage() {
  return (

        <div className="flex h-full w-full bg-black">
          <div className="w-[20%] bg-green-300 p-4">
            <div className="flex flex-col">
              <Upload></Upload>
              <div className="flex justify-center items-center">
                <Pagination></Pagination>
              </div>
            </div>
          </div>
          <div className="w-[80%] bg-yellow-300">
            <div className="grid grid-cols-4 grid-rows-3 gap-5">
              {Array.from({ length: 12 }).map((_, index) => (
                <div key={index} className="bg-white shadow-md">
                  <Song title={`Song ${index + 1}`} image="def.png"></Song>
                </div>
              ))}
            </div>
          </div>
        </div>
  );
}
