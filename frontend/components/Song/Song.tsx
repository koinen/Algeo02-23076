import { Card, CardContent, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";

export interface SongProps {
  fileName: number | string;
  mapping: {
    artist?: string;
    title?: string;
    image?: string;
  };
}

const Song: React.FC<SongProps> = ({ fileName, mapping }) => {
  let imagePath = "";
  if (mapping?.image === "def.png") {
    imagePath = `/album/${mapping?.image}`;
  } else {
    imagePath = `/extracted/${mapping?.image}`;
  }

  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Card className="p-4 h-fit bg-inherit">
          <CardContent className="flex flex-col justify-center items-center">
            <Image
              className="border-4 border-solid border-black"
              src={imagePath}
              alt={"Not Found"}
              width={283}
              height={100}
            ></Image>
            <br />
            {fileName.toString().endsWith(".mid") ? (
              <p>Cannot play MIDI file</p>
            ) : (
              <audio src={`/extracted/${fileName}`} controls />
            )}
            <br />
            <CardTitle className="border-4 border-solid border-black w-full">
              {mapping?.title}
            </CardTitle>
          </CardContent>
        </Card>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="flex justify-between space-x-4">
          <div className="space-y-1">
            <p className="text-sm">Artist : {mapping?.artist}</p>
            <p className="text-sm">File Name : {fileName}</p>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
};

export default Song;
