import cv2
import numpy as np

# 구조 요소 및 반복 횟수 설정
se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
k = 5 # k값 감소 시 뒷번호가 더 잘 검출됨 k값 증가 시 앞번호가 더 잘 검출됨

# 종횡비와 면적 조건 검증 함수
def verify_aspect_size(size):
    w, h = size
    if h == 0 or w == 0: return False
    aspect = h/ w if h > w else w/ h       # 종횡비계산
    chk1 = 3000 < (h * w) < 12000  # 번호판넓이조건
    chk2 = 2.0 < aspect < 6.5       # 번호판종횡비조건
    return (chk1 and chk2)

# 이미지 처리 반복
for i in range(6):  # 6번 반복
    car_no = input("자동차 영상 번호 (00~05): ")
    img = cv2.imread(f'cars/{car_no}.jpg')

    # 전처리
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))

    # 세로 에지 검출
    sobel_grad = cv2.Sobel(blur, cv2.CV_32F, 1, 0, ksize=3)
    sobel = cv2.convertScaleAbs(sobel_grad)

    # 임계값을 이용한 검은 배경과 흰 에지 분리
    ret, binary_img = cv2.threshold(sobel, 120, 255, cv2.THRESH_BINARY)

    # 가로로 긴 구조요소를 이용한 여러번의 닫힘(close)를 통해 흰숫자 에지를 팽창한 후 원상태로 침식
    b_closing = cv2.erode(cv2.dilate(binary_img, se2, iterations=k), se2, iterations=k)  # k = 2
    b_closing = cv2.morphologyEx(b_closing, cv2.MORPH_CLOSE, se2)

    # 윤곽선 검출 및 최소 사각형 추출
    contours, _ = cv2.findContours(b_closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int64(box)

        width, height = rect[1]

        # 종횡비와 면적 조건 만족 여부 확인
        if verify_aspect_size((width, height)):
            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)  # 번호판 후보 표시

    cv2.imshow(f'Binary {car_no}', b_closing)
    # 결과 이미지 보여줌
    cv2.imshow(f'Result {car_no}', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
