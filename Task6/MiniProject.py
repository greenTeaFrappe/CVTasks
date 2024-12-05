import cv2
import sys
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocessing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # BGR 컬러 영상을 명암 영상으로 변환하여 저장
    blur = cv2.blur(gray, (5, 5))
    sobel = cv2.Sobel(blur, cv2.CV_8U, 1, 0, 3)
    _, b_img = cv2.threshold(sobel, 120, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 17), np.uint8)
    morph = cv2.morphologyEx(b_img, cv2.MORPH_CLOSE, kernel, iterations=3)
    return morph

def find_candidates(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects = [cv2.minAreaRect(c) for c in contours]  # 외곽 최소 영역
    candidates = [(tuple(map(int, center)), tuple(map(int, size)), angle)
                  for center, size, angle in rects if verify_aspect_size(size)]

    candidates.sort(key=lambda candidate: candidate[1][0] * candidate[1][1], reverse=True)

    if candidates:
        # 가장 큰 후보만 선택해서 반환
        return [candidates[0]]
    else:
        return []

    return candidates

def verify_aspect_size(size):
    w, h = size
    if h == 0 or w == 0: return False

    aspect = h / w if h > w else w / h  # 종횡비 계산

    chk1 = 3000 < (h * w) < 12000  # 번호판 넓이 조건
    chk2 = 4.0 < aspect < 6.5 # 번호판 종횡비 조건

    return chk1 and chk2

car_no = str(input("자동차 영상 번호 (00~09): "))
img = cv2.imread('cars/' + car_no + '.jpg')
if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

# 1 전처리 단계
preprocessed = preprocessing(img)

# 2 번호판 후보 영역 검출
candidates = find_candidates(preprocessed)

for candidate in candidates:
    pts = np.int32(cv2.boxPoints(candidate))
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect

    if x < 0: x = 0
    if y < 0: y = 0

    if w > 0 and h > 0:
        img1 = img[y:y + h, x:x + w]
        if img1.size > 0:
            gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            _, img_B = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

            text = pytesseract.image_to_string(img_B, config='--psm 8', lang='kor')
            recognized_text = text.strip()

            cv2.imshow('Candidate', img_B)
            print("Recognized Text:", recognized_text)

cv2.waitKey()
cv2.destroyAllWindows()
