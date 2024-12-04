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
  itemsPerPage: number;
  currentPage: number;
  setCurrentPage: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({
  totalItems,
  itemsPerPage,
  currentPage,
  setCurrentPage,
}) => {
  let totalPages = Math.ceil(totalItems / itemsPerPage);

  if (totalPages === 0) {
    totalPages = 1;
  }

  const handleNext = () => {
    if (currentPage < totalPages - 1) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevious = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <Carousel className="w-[50%] max-w-sm">
      <CarouselContent className="-ml-1">
        {Array.from({ length: totalPages }).map((_, index) => (
          <CarouselItem
            key={index}
            className={`pl-1 basis-full ${
              index === currentPage ? "active" : ""
            }`}
          >
            <div className="p-10">
              <Card>
                <CardContent className="flex aspect-square items-center justify-center p-2">
                  <span className="text-2xl font-semibold">{index + 1}</span>
                </CardContent>
              </Card>
            </div>
          </CarouselItem>
        ))}
      </CarouselContent>
      <div onClick={handlePrevious}>
        <CarouselPrevious />
      </div>
      <div onClick={handleNext}>
        <CarouselNext />
      </div>
    </Carousel>
  );
};

export default Pagination;
