import os
import cv2
import easyocr
from datetime import datetime, timedelta


class MegaphoneOCRProcessor:
    """확성기 블록 분리 + OCR 수행 클래스"""

    def __init__(self, megaphone_roi, output_directory, ocr_languages=None):
        """
        :param megaphone_roi: 확성기 영역 ROI (x, y, w, h)
        :param output_directory: 결과 저장 디렉토리
        :param ocr_languages: OCR 언어 설정 (리스트 형식, 예: ["en", "ko"])
        """
        self.megaphone_roi = megaphone_roi
        self.output_directory = output_directory
        self.ocr_languages = ocr_languages if ocr_languages else ["ko", "en"]
        self.reader = easyocr.Reader(self.ocr_languages, gpu=False)

        # 결과 저장 디렉토리 생성
        os.makedirs(self.output_directory, exist_ok=True)

    @staticmethod
    def _round_to_nearest_five(dt):
        """시간을 가장 가까운 5초 단위로 반올림"""
        seconds = (dt.second // 5) * 5
        if dt.second % 5 >= 3:
            seconds += 5
        rounded_time = dt.replace(second=0, microsecond=0) + timedelta(seconds=seconds)
        return rounded_time

    def extract_megaphone(self, screenshot_path):
        """확성기 영역 추출"""
        image = cv2.imread(screenshot_path)
        if image is None:
            print("이미지를 불러오지 못했습니다.")
            return None

        file_creation_time = datetime.fromtimestamp(os.path.getctime(screenshot_path))
        rounded_time = self._round_to_nearest_five(file_creation_time)
        rounded_time_str = rounded_time.strftime("%Y.%m.%d_%H.%M.%S")

        x, y, w, h = self.megaphone_roi
        megaphone_region = image[y:y + h, x:x + w]

        filename = f"megaphone_Screenshot_{rounded_time_str}.png"
        path = os.path.join(self.output_directory, filename)
        cv2.imwrite(path, megaphone_region)

        print(f"확성기 이미지 영역 저장 완료: {path}")
        return path

    def _extract_blocks(self, megaphone_image):
        """확성기 블록 분리 (윤곽선 기반)"""
        gray = cv2.cvtColor(megaphone_image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blocks = []

        for cnt in sorted(contours, key=lambda c: cv2.boundingRect(c)[1]):  # y 기준 정렬
            x, y, w, h = cv2.boundingRect(cnt)

            # 블록 크기 조건에 따라 필터링 (필요 시 조정)
            if w > 500 and h > 30:
                block_img = megaphone_image[y:y+h, x:x+w]
                blocks.append((block_img, (x, y, w, h)))

        return blocks

    def execute_ocr(self, image_path):
        """OCR 수행 (블록 단위)"""
        image = cv2.imread(image_path)
        if image is None:
            print("OCR 이미지를 불러오지 못했습니다.")
            return None

        try:
            blocks = self._extract_blocks(image)
            all_texts = []

            base_filename = os.path.splitext(os.path.basename(image_path))[0]

            for i, (block, _) in enumerate(blocks):
                results = self.reader.readtext(block, detail=0)
                text = " ".join(results).strip()
                all_texts.append(text)

                # 블록 이미지 저장
                block_filename = f"{base_filename}_block{i+1}.png"
                cv2.imwrite(os.path.join(self.output_directory, block_filename), block)

            # 텍스트 저장
            text_filename = base_filename + ".txt"
            text_path = os.path.join(self.output_directory, text_filename)

            with open(text_path, "w", encoding="utf-8") as f:
                f.write("\n".join(all_texts))

            print(f"OCR 결과 저장 완료: {text_path}")
            return all_texts

        except Exception as e:
            print(f"OCR 처리 중 오류 발생: {e}")
            return None

    def process(self, screenshot_path):
        """전체 파이프라인 처리"""
        megaphone_image_path = self.extract_megaphone(screenshot_path)
        if not megaphone_image_path:
            return None
        return self.execute_ocr(megaphone_image_path)
