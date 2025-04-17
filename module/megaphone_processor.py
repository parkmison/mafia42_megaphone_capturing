import os
import cv2
from datetime import datetime, timedelta


class MegaphoneProcessor:
    """스크린샷에서 확성기 영역을 추출"""

    def __init__(self, megaphone_roi, output_directory):
        self.megaphone_roi = megaphone_roi
        self.output_directory = output_directory
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

    @staticmethod
    def _round_to_nearest_five(dt):
        """시간을 가장 가까운 5초 단위로 반올림"""
        seconds = (dt.second // 5) * 5
        if dt.second % 5 >= 3:
            seconds += 5  # 5초 반올림
        rounded_time = dt.replace(second=seconds, microsecond=0)
        if seconds >= 60:  # 분 단위를 넘어가는 경우 처리
            rounded_time += timedelta(minutes=1)
            rounded_time = rounded_time.replace(second=0)
        return rounded_time

    def extract_megaphone(self, screenshot_path):
        """확성기 영역 추출 및 시간 조정 파일 이름으로 저장"""
        image = cv2.imread(screenshot_path)
        if image is None:
            print("스크린샷 이미지를 불러오지 못했습니다.")
            return None

        # 기존 스크린샷의 파일명을 가져옴
        screenshot_filename = os.path.basename(screenshot_path)

        # 스크린샷의 파일 생성 시간을 얻음
        file_creation_time = datetime.fromtimestamp(os.path.getctime(screenshot_path))

        # 시간을 5초 반올림으로 맞추기
        rounded_time = self._round_to_nearest_five(file_creation_time)
        rounded_time_str = rounded_time.strftime("%Y.%m.%d_%H.%M.%S")

        # 새로운 확성기 이미지 저장 이름 생성
        megaphone_filename = f"megaphone_Screenshot_{rounded_time_str}.png"
        megaphone_path = os.path.join(self.output_directory, megaphone_filename)

        # 확성기 영역 추출 및 저장
        x, y, w, h = self.megaphone_roi
        megaphone_region = image[y : y + h, x : x + w]
        cv2.imwrite(megaphone_path, megaphone_region)
        print(f"확성기 영역 저장 완료: {megaphone_path}")
        return megaphone_path
