# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import sys
import PyPDF2
from typing import Callable
import argparse


class RotateClockwise:
    """
    Class that allows for pdf page rotation.
    """

    def __init__(self, toBeRotatedFilePath: str, outputFilePath: str) -> None:
        self.inFile = open(toBeRotatedFilePath, "rb")
        self.pdfRead = PyPDF2.PdfFileReader(self.inFile)
        self.outFile = open(outputFilePath, "wb")

    def __enter__(self) -> RotateClockwise:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.inFile.close()
        self.outFile.close()

    def checkOutfileSize(self) -> None:
        """
        Checks, based on the output file's size, if write is safe.
        By that we mean that there is no content that could be unintentionally modified.
        In case of non-empty file prompts for user input and accordingly either
        continues execution or ends the program.
        :return: None
        """
        if os.stat(self.outFile.name) != 0:
            print(f"Output file {self.outFile.name} is not empty, further \
                program execution may modify it's contents.")
            while True:
                cont: str = input("> Do you wish to continiue? [y/n]").lower()
                if cont in ('y', 'n'):
                    if cont == 'y':
                        break
                    else:
                        sys.exit()
        else:
            pass

    def predicateBased(self, pred: Callable[[int], bool], angleFunc: Callable[[int], int]) -> None:
        """
        Rotates pages indexed from 0 that satisfy pred by angle specified by angleFunc.
        :param pred: (Callable[[int], bool])
         Takes page index and returns information if a given page should be rotated.
        :param angleFunc: (Callable[[int], int])
        for given page index returns angle by which page should be rotated.
        Angle must be one of the following values {0, 90, 180, 270}.
        :return: None
        """
        self.checkOutfileSize()
        pdfWriter = PyPDF2.PdfFileWriter()
        for index, page in enumerate(self.pdfRead.pages):
            if pred(index):
                angle = angleFunc(index)
                if angle in (0, 90, 180, 270):
                    pdfWriter.addPage(page.rotateClockwise(angle))
                else:
                    raise ValueError(f"angleFunc specified attempts to rotate by invalid angle {angle}\n")
        pdfWriter.write(self.outFile)

    def EveryByAngle(self, angle: int) -> None:
        """
        Rotates evey page by angle specified. Angle modulo 360 must be a right angle
        - one of these values {0, 90, 180, 270}.
        :param angle: integer representing the angle of clockwise page rotation.
        :return: None
        """
        self.checkOutfileSize()    
        pdfWriter = PyPDF2.PdfFileWriter()
        for page in self.pdfRead.pages:
            pdfWriter.addPage(page.rotateClockwise(angle % 360))
        pdfWriter.write(self.outFile)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("InputFilePath", help="Path to pdf file that contents are to be manipulated")
    ap.add_argument("OutputFilePath", help="Path and name of new pdf file created by "
                                           "specified modification of Input File")
    args: argparse.Namespace = ap.parse_args()
    with RotateClockwise(args.InputFilePath, args.OutputFilePath) as rotate:
        rotate.predicateBased(lambda i: i == 1, lambda i: 90)


if __name__ == "__main__":
    main()
