# Property of gaspa92™ all rights reserve

import cv2
import numpy as np

img1 = cv2.imread('img0.jpg', cv2.IMREAD_COLOR)
img2 = cv2.imread('img0.jpg', cv2.IMREAD_COLOR)

def get_points_img1(event, x, y, flags, param):
    global img1_points
    global img1_click_n

    if event == cv2.EVENT_LBUTTONDOWN:
        img1_click_n = img1_click_n + 1

        if img1_click_n == 1:
            img1_points[0], img1_points[1] = x, y

        if img1_click_n == 2:
            img1_points[2], img1_points[3] = x, y

        if img1_click_n == 3:
            img1_points[4], img1_points[5] = x, y
            print(img1_points[0], img1_points[1], img1_points[2], img1_points[3], img1_points[4], img1_points[5])

def get_points_img2(event, x, y, flags, param):
    global img2_points
    global img2_click_n

    if event == cv2.EVENT_LBUTTONDOWN:
        img2_click_n = img2_click_n + 1

        if img2_click_n == 1:
            img2_points[0], img2_points[1] = x, y

        if img2_click_n == 2:
            img2_points[2], img2_points[3] = x, y

        if img2_click_n == 3:
            img2_points[4], img2_points[5] = x, y
            print(img2_points[0], img2_points[1], img2_points[2], img2_points[3], img2_points[4], img2_points[5])


def eucl_transform(img, angle, tx, ty):
    img_h, img_w, img_c = np.shape(img)

    M = cv2.getRotationMatrix2D((img_h/2, img_w/2), angle, 1)
    M[0, 2] = tx
    M[1, 2] = ty
    print(M)
    img_temp = cv2.warpAffine(img, M, (img_w, img_h))

    return img_temp


img1_click_n = 0
img1_points = [-1, -1, -1, -1, -1, -1]
img2_click_n = 0
img2_points = [-1, -1, -1, -1, -1, -1]

cv2.namedWindow('image1')
cv2.namedWindow('image2')
cv2.setMouseCallback('image1', get_points_img1)
cv2.setMouseCallback('image2', get_points_img2)

while(1):
    cv2.imshow('image1', img1)
    cv2.imshow('image2', img2)

    # -------------- Inputs -----------------
    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        break

    elif k == 27:
        break
    # ---------------------------------------

    if img1_click_n == 3 and img2_click_n == 3:
        pts1 = np.float32([[img1_points[0],img1_points[1]],[img1_points[2],img1_points[3]],[img1_points[4],img1_points[5]]])
        pts2 = np.float32([[img2_points[0],img2_points[1]],[img2_points[2],img2_points[3]],[img2_points[4],img2_points[5]]])

        M = cv2.getAffineTransform(pts1, pts2)

        img1_h, img1_w, img1_c = np.shape(img1)
        cv2.warpAffine(img2, M, (img1_w, img1_h), img1)

cv2.destroyAllWindows()
