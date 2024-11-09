import cv2

# 좌표를 출력할 콜백 함수
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭 시
        print(f"좌표: x={x}, y={y}")

# 이미지 불러오기
img = cv2.imread('.\\object_images\\clover.jpeg')
scale_percent = 70  # 50% 크기로 축소
height, width = img.shape[:2]
new_width = int(width * scale_percent / 100)
new_height = int(height * scale_percent / 100)
img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

cv2.imwrite('./object_images/clover.jpeg', img)
cv2.imshow('Image', img)

# 마우스 이벤트 설정
cv2.setMouseCallback('Image', get_coordinates)

cv2.waitKey(0)
cv2.destroyAllWindows()
