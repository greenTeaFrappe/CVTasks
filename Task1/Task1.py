import math

import cv2
import numpy as np

img = np.ones((600, 900, 3), np.uint8) * 255  # 캔버스 600*900 흰색으로 설정

frame = img  # 이미지 저장할 frame 초기화


def draw(event, x, y, flags, param):  # 마우스 콜백 함수
    global ix, iy  # 시작 좌표 저장 변수

    BrushSiz = 5  # 브러쉬 사이즈 설정
    BColor, RColor, GColor, YColor = (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 255, 255)  # 사용할 색상

    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼을 눌렀을 때
        if flags & cv2.EVENT_FLAG_ALTKEY:  # ALT를 누른다면
            ix, iy = x, y  # 누른 시점의 좌표값 저장
        elif flags & cv2.EVENT_FLAG_CTRLKEY:  # CTRL을 누른다면
            ix, iy = x, y  # 누른 시점의 좌표값 저장
    elif event == cv2.EVENT_LBUTTONUP:  # 마우스 왼쪽 버튼을 땠을 때
        if flags & cv2.EVENT_FLAG_ALTKEY:  # ALT를 누르는 중이면
            cv2.rectangle(img, (ix, iy), (x, y), BColor, 2)  # img에 ix,iy에서 시작하고 현재 x,y에서 끝나는 BColor의 선 두께 2인 직사각형 생성
        elif flags & cv2.EVENT_FLAG_CTRLKEY:  # CTRL을 누르는 중이면
            cv2.circle(img, (ix, iy), int(math.sqrt((x - ix) ** 2 + (y - iy) ** 2)), RColor, 2)
            # img에 ix,iy가 중심점이며 현재 x,y와 ix,iy 사이의 거리를 반지름으로 하는 RColor의 선 두께 2인 원 생성

    elif event == cv2.EVENT_RBUTTONDOWN:  # 마우스 오른쪽 버튼을 눌렀을 때
        if flags & cv2.EVENT_FLAG_ALTKEY:  # ALT를 누른다면
            ix, iy = x, y  # 누른 시점의 좌표값 저장
        elif flags & cv2.EVENT_FLAG_CTRLKEY:  # CTRL을 누른다면
            ix, iy = x, y  # 누른 시점의 좌표값 저장
    elif event == cv2.EVENT_RBUTTONUP:  # 마우스의 오른쪽 버튼을 땠을 때
        if flags & cv2.EVENT_FLAG_ALTKEY:  # ALT를 누르는 중이면
            cv2.rectangle(img, (ix, iy), (x, y), BColor, -1)  # img에 ix,iy에서 시작하고 현재 x,y에서 끝나는 BColor의 내부가 채워진 직사각형 생성
        elif flags & cv2.EVENT_FLAG_CTRLKEY:  # CTRL을 누르는 중이면
            cv2.circle(img, (ix, iy), int(math.sqrt((x - ix) ** 2 + (y - iy) ** 2)), RColor, -1)
            # img에 ix,iy가 중심점이며 현재 x,y와 ix,iy 사이의 거리를 반지름으로 하는 RColor의 내부가 채워진 2인 원 생성

    elif event == cv2.EVENT_MOUSEMOVE:  # 마우스를 움직이고 있을 때
        # ALT키/CTRL키/SHIFT키가 눌리지 않은 상태에서만 실행
        if not (flags & cv2.EVENT_FLAG_ALTKEY) and not (flags & cv2.EVENT_FLAG_CTRLKEY) and not (
                flags & cv2.EVENT_FLAG_SHIFTKEY):
            if flags & cv2.EVENT_FLAG_LBUTTON:  # 왼쪽 버튼을 클릭 했을 때
                cv2.circle(img, (x, y), BrushSiz, BColor, -1)  # img에 현재 위치를 중심으로 하는 BColor의 반지름이 5인 내부가 채워진 원 계속 생성
            elif flags & cv2.EVENT_FLAG_RBUTTON:  # 오른쪽 버튼을 클릭 했을 때
                cv2.circle(img, (x, y), BrushSiz, RColor, -1)  # img에 현재 위치를 중심으로 하는 RColor의 반지름이 5인 내부가 채워진 원 계속 생성
        elif flags & cv2.EVENT_FLAG_SHIFTKEY:  # SHIFT가 눌리고 있다면
            if flags & cv2.EVENT_FLAG_LBUTTON:  # 왼쪽 버튼을 클릭 했을 때
                cv2.circle(img, (x, y), BrushSiz, GColor, -1)  # img에 현재 위치를 중심으로 하는 GColor의 반지름이 5인 내부가 채워진 원 계속 생성
            elif flags & cv2.EVENT_FLAG_RBUTTON:  # 오른쪽 버튼을 클릭 했을 때
                cv2.circle(img, (x, y), BrushSiz, YColor, -1)  # img에 현재 위치를 중심으로 하는 YColor의 반지름이 5인 내부가 채워진 원 계속 생성

    cv2.imshow('Drawing', img)


cv2.namedWindow('Drawing')
cv2.imshow('Drawing', img)

cv2.setMouseCallback('Drawing', draw)

while True:
    key = cv2.waitKey(1)  # 키 입력을 한 번만 호출하여 저장

    if key == ord('q'):  # 'q' 키가 눌리면 종료
        cv2.destroyAllWindows()
        break
    elif key == ord('s'):  # 's' 키가 눌리면 캡처 및 저장
        cv2.imwrite('captured.png', frame)
