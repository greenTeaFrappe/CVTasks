import sys
import cv2

cap = cv2.VideoCapture('cat...!.mp4')

if not cap.isOpened():
    sys.exit('동영상 연결 실패')

frame1 = None

while True:
    ret, frame = cap.read()  # 비디오를 구성하는 프레임 획득

    if not ret:
        print('프레임 획득에 실패하여 루프를 나갑니다.')
        break

    # frame1이 없다면 원본을 출력
    if frame1 is None:
        cv2.imshow('Video display', frame)
    else:
        cv2.imshow('Video display', frame1)  # 효과가 적용된 프레임을 보여줌

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('n'):   # 오리지널
        frame1 = frame.copy()
        cv2.putText(frame1, 'Original', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    elif key == ord('b'):   # bilateral
        frame1 = cv2.bilateralFilter(frame, -1, 10, 5)
        cv2.putText(frame1, 'Bilateral', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    elif key == ord('s'):   # stylization
        frame1 = cv2.stylization(frame, sigma_s=60, sigma_r=0.45)
        cv2.putText(frame1, 'Stylization', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    elif key == ord('g'):   # Gray pencilSketch
        frame1, _ = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.7, shade_factor=0.02)
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_GRAY2BGR)  # 그레이 이미지를 컬러로 변환해서 같은 창에 출력
        cv2.putText(frame1, 'Gray pencilSketch', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    elif key == ord('c'):   # Color pencilSketch
        _, frame1 = cv2.pencilSketch(frame, sigma_s=60, sigma_r=0.7, shade_factor=0.02)
        cv2.putText(frame1, 'Color pencilSketch', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)
    elif key == ord('o'):   # Oil Painting
        frame1 = cv2.xphoto.oilPainting(frame, 7, 1)
        cv2.putText(frame1, 'Oil Painting', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 100), 2)

cap.release()  # 카메라와 연결을 끊음
cv2.destroyAllWindows()
