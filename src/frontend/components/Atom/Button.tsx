"use client";

import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";

interface ButtonProps {
  text: string;
}

const ButtonLight: React.FC<ButtonProps> = ({ text }) => {
  return (
    <Button variant="outline">
      <p className="p-7">{text}</p>
    </Button>
  );
};

const ButtonLoading: React.FC = () => {
  return (
    <Button disabled>
      <Loader2 className="animate-spin" />
      Please wait
    </Button>
  );
};

export { ButtonLight, ButtonLoading };