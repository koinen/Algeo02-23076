import { Card, CardContent } from "@/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import React from "react";

interface PaginationProps {
  totalItems: number;
  currentPage: number;
  setCurrentPage: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({
  totalItems,
  currentPage,
  setCurrentPage,
}) => {
  let totalPages = totalItems;

  if (totalPages === 0) {
    totalPages = 1;
  }

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <Carousel className="w-[10%] flex items-center justify-center">
      <CarouselContent>
        {Array.from({ length: totalPages }).map((_, index) => (
          <CarouselItem
            key={index}
          />
        ))}
      </CarouselContent>
      <div onClick={handleNext}>
        <CarouselNext />
      </div>
    </Carousel>
  );
};

export default Pagination;
