# 대충 마피아 확성기 찍어서 5초마다 올리는거 어쩌구 저쩌구 
블루스택 : 
세로모드,

픽셀밀도 320DPI

성능 : 높음 (메모리등 포함)

프레임 : 30 

핸드폰 : 삼성 갤럭시 S21 Ultra임 
(이건걍 내가 임의로한설정)

단축키에서 스크린샷키 F8로 변경


# 그래서 뭐하는데
블루스택-마피아42-채널에 들어가서 확성기창 켜놓은상태로 있으면

얘가 캡쳐해서 저장해줌

원본은 원본 주소가 저장되는 폴더를 main_controller.py에서 바꿔줘야함

그리고 그걸 받아서 해상도에 맞게 확성기쪽만 크롭함

지금은 여기까지만 했음 

OCR은 엄두도안난다

--- 이상 250417---ㅇㅇㅇ 

-250418_v1
easyocr로 바꿈 pip install easyocr

근데 이거 뭔가 처리속도가 좀 오래걸림 

GPU를 쓰면 더 잘된다는데 내장CPU라 엄두가 안남 

-250418_v2
megaphone_ocr_processor.py로 두가지 모듈을 통합함 (그냥 스크린샷 바로 잘라)

main_controller를 조금 수정함 (모듈이 바뀌었으니)

블록화는 괜찮아보이지만 더 수정해야함 

-250419_v1

스크린샷을 블록화해서 개별단위로 저장하게 하고 개별단위의 OCR을 적용해서 파일을 저장하게끔 함

