import React from "react";
import Image from "next/image";

const NotFound: React.FC = () => {
  return (
    <div className="flex flex-col items-center h-full w-full bg-white">
        <Image src={"/404.gif"} alt="404" width={800} height={800} unoptimized></Image>
      <p className="text-2xl">404</p>
      <p className="text-2xl">Not Found</p>
    </div>
  );
};

export default NotFound;
