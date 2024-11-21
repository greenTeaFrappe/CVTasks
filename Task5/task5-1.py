import cv2
import sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # Face 분류기 로드

def face_sticker(num):
    img = cv2.imread(f'yys/yys{num}.jpg')
    if img is None:
        sys.exit('파일을 찾을 수 없습니다.')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 그레이 이미지로 변환
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # 얼굴 검출

    face_mask=cv2.imread('y_sticker.jpg')
    h_mask, w_mask = face_mask.shape[:2]

    for (x,y,w,h) in faces:
        if h > 0 and w > 0:
            roi = img[y:y+h, x:x+w]   # 검출된 얼굴에 대한 사각형 영역을 관심 영역(ROI)로 설정

            face_mask_small=cv2.resize(face_mask,(w,h),interpolation=cv2.INTER_AREA) # 가면 이미지의 크기를 검출된 얼굴의 크기와 같도록 resize

            gray_mask = cv2.cvtColor(face_mask_small, cv2.COLOR_BGR2GRAY) # ① 가면 마스크에서 검지 않은 부분만 통과(검은색 부분은 투명)
            ret, mask = cv2.threshold(gray_mask, 254, 255, cv2.THRESH_BINARY_INV)
            masked_face = cv2.bitwise_and(face_mask_small, face_mask_small, mask=mask)

            mask_inv = cv2.bitwise_not(mask)  # ② 검출된 얼굴에서 가면 마스크의 검은 부분만 통과(검지 않은 부분은 투명)
            masked_img = cv2.bitwise_and(roi, roi, mask=mask_inv)

            img[y:y+h, x:x+w] = cv2.add(masked_face, masked_img) # 흰색 마스크와 마스크된 얼굴 합성 (① + ②)

            cv2.imshow(f'sticker_face_{num}',img)
            cv2.imwrite(f'sticker_yys/sticker_yys_{num}.jpg',img)

for i in range(5):
    face_sticker(i)

cv2.waitKey()
cv2.destroyAllWindows()