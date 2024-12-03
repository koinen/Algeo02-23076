import {
  Card,
  CardContent,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";

interface SongProps {
  title: string;
  image: string;
}

const Song: React.FC<SongProps> = ({ title, image }) => {

  const imagePath = `/album/${image}`;

  return (
    <Card className="p-4 h-fit bg-inherit">

      <CardContent className="flex flex-col justify-center items-center">
        <Image className="border-4 border-solid border-black" src={imagePath} alt={title} width={300} height={400}></Image>
        <CardTitle className="border-4 border-solid border-black w-full">{title}</CardTitle>
      </CardContent>
    </Card>
  );
};

export default Song;
