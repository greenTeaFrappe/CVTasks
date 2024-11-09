import cv2
import os

stitcher = cv2.Stitcher.create()
images = []

# 1-1 stitch 이미지 불러오기
images.append(cv2.imread('.\\stitch_images\\img1.jpg'))
images.append(cv2.imread('.\\stitch_images\\img2.jpg'))
images.append(cv2.imread('.\\stitch_images\\img3.jpg'))
images.append(cv2.imread('.\\stitch_images\\img4.jpg'))

# 2-2 모든 이미지를 한까번에 stitch 수행
status, dst = stitcher.stitch((images[0],images[1],images[2],images[3]))
#status, dst = stitcher.stitch(images)

if status == cv2.STITCHER_OK:
    cv2.imwrite('.\stitch_images\stitch_out.jpg', dst)
    cv2.imshow('stitching',  dst)

cv2.waitKey()
cv2.destroyAllWindows()