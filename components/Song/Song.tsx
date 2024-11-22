import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import Image from "next/image";

const Song: React.FC = () => {
  return (
    <Card className="p-4 h-fit bg-inherit">
      <CardContent className="flex flex-col justify-center items-center">
        <Image className="border-4 border-solid border-black" src="/images/Album.jpg" alt="Album" width={300} height={200}></Image>
        <CardTitle className="border-4 border-solid border-black w-full">Nama Lagu</CardTitle>
      </CardContent>
    </Card>
  );
};

export default Song;
