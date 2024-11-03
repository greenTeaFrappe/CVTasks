import cv2

se2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
k = 2

for i in range(0,6): # 6번 반복
    gray=cv2.imread(f'0{i}.jpg',cv2.IMREAD_GRAYSCALE) # 이미지 가져오기
    blur=cv2.blur(gray, (3, 3)) # 전처리

    # 세로 에지 검출
    sobel_grad=cv2.Sobel(blur,cv2.CV_32F,1,0,ksize=3)
    sobel = cv2.convertScaleAbs(sobel_grad)

    # 임계값을 이용한 검은 배경과 흰 에지 분리
    ret, binary_img = cv2.threshold(sobel, 120, 255, cv2.THRESH_BINARY)

    # 가로로 긴 구조요소를 이용한 여러번의 닫힘(close)를 통해 흰숫자 에지를 팽창한 후 원상태로 침식
    b_closing = cv2.erode(cv2.dilate(binary_img,se2,iterations=k),se2,iterations=k) # k = 2
    b_closing = cv2.morphologyEx(b_closing, cv2.MORPH_CLOSE, se2)

    # 이미지 보여줌
    cv2.imshow(f'result{i}', b_closing)

cv2.waitKey()
cv2.destroyAllWindows()