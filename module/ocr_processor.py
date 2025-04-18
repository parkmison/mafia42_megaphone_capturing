import os
import cv2
import easyocr


class OCRProcessor:
    """OCR 처리 클래스 (EasyOCR 기반)"""

    def __init__(self, output_directory, languages=["ko"]):
        """
        :param output_directory: OCR 결과를 저장할 디렉토리
        :param languages: 사용할 언어 설정 (리스트 형식, 예: ["en", "ko"])
        """
        self.output_directory = output_directory
        self.reader = easyocr.Reader(languages, gpu=False)  # GPU를 사용하려면 gpu=True로 설정

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    def extract_text(self, image_path):
        """OCR로 텍스트 추출 및 저장"""
        # 이미지 파일명에서 텍스트 파일명 생성
        image_filename = os.path.basename(image_path)
        name_without_extension = os.path.splitext(image_filename)[0]
        text_filename = f"{name_without_extension}.txt"
        output_path = os.path.join(self.output_directory, text_filename)

        # 이미지 로드 및 검증
        image = cv2.imread(image_path)
        if image is None:
            print("OCR 이미지 불러오기를 실패했습니다.")
            return None

        # EasyOCR로 텍스트 추출
        try:
            results = self.reader.readtext(image_path, detail=0)  # detail=0은 텍스트만 반환
            extracted_text = "\n".join(results)

            # 추출된 텍스트 저장
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(extracted_text)

            print(f"OCR 텍스트 저장 완료: {output_path}")
            return output_path

        except Exception as e:
            print(f"OCR 처리 중 오류 발생: {e}")
            return None
