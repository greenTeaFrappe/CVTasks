import cv2
import numpy as np

# 비디오 파일을 열기
cap = cv2.VideoCapture('rps.mp4')

# 피부색 범위 설정 (HSV 값)
lower_skin = np.array([8, 50, 150], dtype=np.uint8)
upper_skin = np.array([14, 160, 255], dtype=np.uint8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임 크기 조정
    output_width, output_height = 500, 888
    frame = cv2.resize(frame, (output_width, output_height))

    # BGR 이미지를 HSV로 변환 후 피부색 범위에 해당하는 마스크 생성
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # 윤곽선 찾기
    try:
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    except Exception as e:
        print(f"Error in findContours: {e}")
        continue

    # 윤곽선이 없을 때는 다음 프레임으로
    if len(contours) == 0:
        continue

    # 가장 큰 윤곽선을 선택
    contour = max(contours, key=cv2.contourArea)

    # 윤곽선을 프레임에 그리기 (파란색)
    cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)

    # Convex Hull 계산
    try:
        hull = cv2.convexHull(contour, returnPoints=False)
        defects = cv2.convexityDefects(contour, hull)
    except Exception as e:
        continue

    # 결과 출력
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", frame)

    # 'q' 키로 종료
    key = cv2.waitKey(30)
    if key == ord('q'):
        break

# 비디오 캡처 객체 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
