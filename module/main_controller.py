import os
import time
from datetime import datetime, timedelta, timezone

from module.bluestacks_manager import BluestacksManager
from module.screenshot_controller import ScreenshotController
from module.megaphone_processor import MegaphoneProcessor
from module.ocr_processor import OCRProcessor



class MainController:
    """프로그램 실행 컨트롤러"""

    def __init__(self):
        self.base_path = "D:/python/mafia42_megaphone_new1"
        self.screenshot_dir = os.path.join(self.base_path, "mafia42screenshots")
        self.megaphone_dir = os.path.join(self.base_path, "megaphone_regions")
        self.text_dir = os.path.join(self.base_path, "output_texts")
        self.megaphone_roi = (266, 615, 548, 596)

        for directory in [self.megaphone_dir, self.text_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def execute_actions(self):
        """한 번의 작업 실행"""
        bluestacks_manager = BluestacksManager()
        if not bluestacks_manager.find_and_activate():
            return False

        screenshot_controller = ScreenshotController(self.screenshot_dir)
        screenshot_file = screenshot_controller.capture()
        if not screenshot_file:
            return False

        megaphone_processor = MegaphoneProcessor(self.megaphone_roi, self.megaphone_dir)
        megaphone_file = megaphone_processor.extract_megaphone(screenshot_file)
        if not megaphone_file:
            return False

        ocr_processor = OCRProcessor(self.text_dir)
        if not ocr_processor.extract_text(megaphone_file):
            return False

        print("작업 완료.")
        return True

    def run(self):
        """UTC 기준 5초 배수에 맞춰 반복 작업 실행"""
        print("UTC 기준 5초 간격 작업을 시작합니다.")
        while True:
            # 현재 시간 (UTC 기준)
            now = datetime.now(timezone.utc)

            # 5초 배수의 시간으로 맞추기
            next_run_time = now + timedelta(seconds=(5 - now.second % 5))  # 5초 남은 시간 계산
            wait_time = (next_run_time - datetime.now(timezone.utc)).total_seconds()

            print(f"다음 작업 예약 시간 (UTC): {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}. 대기: {wait_time:.2f}초")

            # 작업 실행
            time.sleep(max(wait_time, 0))  # 음수가 되지 않게 처리
            self.execute_actions()
