import os
import time
from datetime import datetime, timedelta, timezone
from module.megaphone_ocr_processor import MegaphoneOCRProcessor
from module.bluestacks_manager import BluestacksManager
from module.screenshot_controller import ScreenshotController


class MainController:
    """프로그램 실행 컨트롤러"""

    def __init__(self):
        self.base_path = "D:/python/mafia42_megaphone_new1"
        self.screenshot_dir = os.path.join(self.base_path, "mafia42screenshots")
        self.output_dir = os.path.join(self.base_path, "output_texts")
        self.megaphone_roi = (266, 615, 548, 596)

        # 디렉토리 생성
        for directory in [self.screenshot_dir, self.output_dir]:
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

        # MegaphoneOCRProcessor 실행
        processor = MegaphoneOCRProcessor(self.megaphone_roi, self.output_dir, ["ko", "en"])
        ocr_result = processor.process(screenshot_file)
        if not ocr_result:
            return False

        print(f"OCR 결과:\n{ocr_result}")
        return True

    def run(self):
        """UTC 기준 5초 배수에 맞춰 반복 작업 실행"""
        print("UTC 기준 5초 간격 작업을 시작합니다.")
        while True:
            try:
                # 현재 시간 (UTC 기준)
                now = datetime.now(timezone.utc)

                # 5초 배수의 시간으로 맞추기
                next_run_time = now + timedelta(seconds=(5 - now.second % 5))
                wait_time = (next_run_time - datetime.now(timezone.utc)).total_seconds()

                print(f"다음 작업 예약 시간 (UTC): {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}. 대기: {wait_time:.2f}초")

                # 기다리기
                time.sleep(max(wait_time, 0))

                # 작업 실행
                if self.execute_actions():
                    print("작업이 성공적으로 완료되었습니다.")
                else:
                    print("작업 실행 중 오류 발생.")

            except KeyboardInterrupt:
                print("프로그램이 수동으로 중단되었습니다.")
                break
            except Exception as e:
                print(f"예기치 못한 오류 발생: {e}")
                break