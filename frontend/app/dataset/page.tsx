import { InputPath } from "@/components/InputPath/InputPath";
import Image from "next/image";

export default function DataPage() {
  return (
    <div className="flex flex-col justify-center items-center h-screen">
        <div className="w-[50%] h-fit mb-[20vh] bg-black">
            <div className="bg-purple-400">
                <h1>Dataset Page: None</h1>
                <Image
                    src="/album/def.png" alt="tes" width={500} height={500}>
                </Image>
            </div>
            <div className="bg-yellow-400">
                <InputPath></InputPath>
            </div>
        </div>
    </div>
  );
}
