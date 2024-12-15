import {
  Card,
  CardContent,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"

interface MappingItems {
  artist?: string;
  title?: string;
  image?: string;
}

export interface SongProps {
  fileName: string;
  mapping?: MappingItems;
}

const Song: React.FC<SongProps> = ({ fileName, mapping }) => {

  const imagePath = `${mapping?.image}`;

  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Card className="p-4 h-fit bg-inherit">
          <CardContent className="flex flex-col justify-center items-center">
            <Image className="border-4 border-solid border-black" src={imagePath} alt={"Not Found"} width={283} height={100}></Image>
            <CardTitle className="border-4 border-solid border-black w-full">{mapping?.title}</CardTitle>
          </CardContent>
        </Card>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="flex justify-between space-x-4">
          <div className="space-y-1">
            <p className="text-sm">
              Artist : {mapping?.artist}
            </p>
            <p className="text-sm">
              File Name : {fileName}
            </p>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
};

export default Song;
