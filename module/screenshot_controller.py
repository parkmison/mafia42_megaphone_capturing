import os
import time
import pyautogui
from glob import glob


class ScreenshotController:
    """스크린샷 관리 클래스"""

    def __init__(self, screenshot_dir):
        self.screenshot_dir = screenshot_dir

    def capture(self):
        """F8 키를 눌러 스크린샷 촬영"""
        print("스크린샷 키(F8) 입력 중...")
        pyautogui.hotkey("f8")  # 'F8' 키 입력
        print("스크린샷 키 입력 완료. 스크린샷 저장 대기 중...")

        # 최대 10초 동안 새로 생성된 파일을 검색
        start_time = time.time()
        while time.time() - start_time < 10:
            try:
                latest_screenshot = max(
                    glob(os.path.join(self.screenshot_dir, "Screenshot_*.png")),
                    key=os.path.getctime
                )
                print(f"최신 스크린샷 파일: {latest_screenshot}")
                return latest_screenshot
            except ValueError:
                time.sleep(0.5)  # 파일이 없으면 0.5초간 대기
                continue

        print("스크린샷 파일을 찾을 수 없습니다. 작업을 중지합니다.")
        return None
