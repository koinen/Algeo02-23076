import Image from "next/image";
import Song from "../components/Song/Song";
import ButtonLight from "../components/Atom/Button";
import Pagination from "../components/Pagination/Pagination";
export default function HomePage() {
  return (
    <main className="relative flex flex-col justify-end overflow-hidden">
      <div className="bg-blue-500 h-screen inset-0 w-full">
        <nav className="bg-red-400 p-5 flex flex-row items-center">
          <Image src="/images/logo.jpg" alt="Logo" width={50} height={50} />
          <h1 className="ml-4">this is navbar</h1>
        </nav>
        <div className="flex h-full w-full bg-black">
          <div className="w-[20%] bg-green-300 p-4">
            <div className="flex flex-col">
              <div className="h-max-[25rem]">
                <Song></Song>
              </div>
              <div className="flex h-max-[10rem] justify-center items-center">
                <ButtonLight text="Upload"></ButtonLight>
              </div>
              <div className="flex h-max-[10rem] justify-center items-center mt-10">
                <ButtonLight text="Audios"></ButtonLight>
              </div>
              <div className="flex h-max-[10rem] justify-center items-center mt-3">
                <ButtonLight text="Pictures"></ButtonLight>
              </div>
              <div className="flex h-max-[10rem] justify-center items-center mt-3">
                <ButtonLight text="Mapper"></ButtonLight>
              </div>
              <div className="flex flex-col h-[10rem] justify-center items-center mt-3">
                <p>tes</p>
                <p>tes</p>
                <p>tes</p>
              </div>
              <div className="flex justify-center items-center">
                <Pagination></Pagination>
              </div>
            </div>
          </div>
          <div className="w-[80%] bg-yellow-300">
          <div className="grid grid-cols-4 grid-rows-3 gap-5">
            {Array.from({ length: 12 }).map((_, index) => (
              <div key={index} className="bg-white shadow-md">
                <Song></Song>
              </div>
            ))}
          </div>
          </div>
        </div>
      </div>
    </main>
  );
}
