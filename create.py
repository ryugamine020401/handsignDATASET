import cv2, os
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# fontFace = cv2.FONT_HERSHEY_SIMPLEX              # 印出文字的字型
# lineType = cv2.LINE_AA                           # 印出文字的邊框
cnt = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'K':0, 'L':0
        , 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0, 'U':0, 'V':0, 'W':0, 'X':0, 'Y':0}

for i in cnt:
        tmp = len(os.listdir(f'./{i}/'))
        cnt[f'{i}'] = tmp
        print(i, tmp, end = "   ")
print()
for i in cnt:
    if (not os.path.isdir(i)):
        print("建立資料夾", i)
        os.mkdir(i)

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)    # 開啟鏡頭
    detector = HandDetector(detectionCon=0.8, maxHands=1)  # 信心程度大於0.5才輸出且最多偵測一隻手
    while 1:        # 當鏡頭打開
        key = cv2.waitKey(1)     # 算出手部位置，且不畫出外框
        success, img = cam.read()  # 取出詳細座標
        ori_img = img
        hands = detector.findHands(img, draw=False)   # hands, img = detector.findHands(img)
        if hands:
            hand1 = hands[0]
            x, y, w, h = hand1['bbox']
            # print(x, y, w, h, sep=' ')
            if w > h:                    # 將長寬變為一致
                y = int(y - (w - h) / 2)
                h = w
            else:
                x = int(x - (h - w) / 2)
                w = h
            ori_img = ori_img[y-25:y+h+25, x-25:x+w+25]  # 裁切
            
            if x-25 > 0 and x+w+25 < 765 and y-25 > 0:  # 若圖片未超出範圍
                cv2.imshow('img2', ori_img)       # 顯示裁切後的圖片
                ## vscode CTRL+K 再 CTRL+C多行註解
                for i in cnt:
                    if(key == ord(i)):
                        print([i, cnt[f'{i}']])
                        cv2.imwrite(f'./{i}/{i+str(cnt[f"{i}"])}.jpg', ori_img)
                        cnt[f'{i}'] += 1
        cv2.imshow("Video", img)        # 顯示原圖

        if key == 27:  # 按ESC or q離開迴圈
            break
    cam.release()
    cv2.destroyAllWindows()