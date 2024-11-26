import { Button } from "@/components/ui/button"

interface ButtonProps {
    text: string;
}

const ButtonLight: React.FC<ButtonProps> = ({ text }) => {
    return (
        <Button variant="outline">
            <p className="p-7">{text}</p>
        </Button>
    );
}

export default ButtonLight;