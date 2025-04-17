import pygetwindow as gw


class BluestacksManager:
    """블루스택 창 관리 클래스"""

    def __init__(self, window_title="Bluestacks"):
        self.window_title = window_title
        self.window = None

    def find_and_activate(self):
        """블루스택 창을 찾고 활성화"""
        windows = gw.getWindowsWithTitle(self.window_title)
        if windows:
            self.window = windows[0]
            self.window.activate()
            print(f"블루스택 창 '{self.window_title}' 활성화 완료!")
            return True
        print("블루스택 창을 찾을 수 없습니다. 실행 중인지 확인해주세요.")
        return False
