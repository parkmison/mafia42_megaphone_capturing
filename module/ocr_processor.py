import os
import cv2
from pytesseract import pytesseract


class OCRProcessor:
    """OCR 처리 클래스"""

    def __init__(self, output_directory, tesseract_cmd="C:/Program Files/Tesseract-OCR/tesseract.exe"):
        self.output_directory = output_directory
        self.tesseract_cmd = tesseract_cmd
        pytesseract.tesseract_cmd = self.tesseract_cmd

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def extract_text(self, image_path):
        """OCR로 텍스트 추출 및 저장"""
        # 이미지 파일명에서 텍스트 파일명 생성
        image_filename = os.path.basename(image_path)
        name_without_extension = os.path.splitext(image_filename)[0]
        text_filename = f"{name_without_extension}.txt"
        output_path = os.path.join(self.output_directory, text_filename)

        # OCR 처리
        image = cv2.imread(image_path)
        if image is None:
            print("OCR 이미지 불러오기를 실패했습니다.")
            return None

        text = pytesseract.image_to_string(image, lang="eng")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"OCR 텍스트 저장 완료: {output_path}")
        return output_path
