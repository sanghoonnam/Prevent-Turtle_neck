import cv2
import mediapipe as mp
import time
import math

class HolisticDetector():
    def __init__(self,
               static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHolistic = mp.solutions.holistic
        self.mpPose = mp.solutions.pose
        self.mpFace = mp.solutions.face_mesh
        self.holistics = self.mpHolistic.Holistic(self.static_image_mode, self.model_complexity, self.smooth_landmarks, self.min_detection_confidence, self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def findHolistic(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB )
        self.results = self.holistics.process(imgRGB)

        if self.results.pose_landmarks:
            
            if draw:
                 # Draw pose, left and right hands, and face landmarks on the image.
                annotated_image = img.copy()

                # self.mpDraw.draw_landmarks(
                #     annotated_image, self.results.face_landmarks, self.mpHolistic.FACE_CONNECTIONS)
                self.mpDraw.draw_landmarks(
                    annotated_image, self.results.left_hand_landmarks, self.mpHolistic.HAND_CONNECTIONS)
                self.mpDraw.draw_landmarks(
                    annotated_image, self.results.right_hand_landmarks, self.mpHolistic.HAND_CONNECTIONS)
                # self.mpDraw.draw_landmarks(
                #     annotated_image, self.results.pose_landmarks, self.mpHolistic.POSE_CONNECTIONS)

                # Plot pose world landmarks.
                # self.mpDraw.plot_landmarks(
                #     self.results.pose_world_landmarks, self.mpHolistic.POSE_CONNECTIONS)
                return annotated_image
            
        return img

    def findPoseLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.pose_lmList = []
        if self.results.pose_landmarks:
            myHolistic = self.results.pose_landmarks
            # print(myHolistic.landmark)
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*(w+h)/2)
                # print(id, cx, cy)
                # print(cz)
                xList.append(cx)
                yList.append(cy)
                self.pose_lmList.append([id, cx, cy, cz])

        return self.pose_lmList

    def findFaceLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.face_lmList = []
        if self.results.face_landmarks:
            myHolistic = self.results.face_landmarks
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*(w+h)/2)
                # print(id, cx, cy)
                xList.append(cx)
                yList.append(cy)
                self.face_lmList.append([id, cx, cy, cz])

        return self.face_lmList

    def findLefthandLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.left_hand_lmList = []
        if self.results.left_hand_landmarks:
            myHolistic = self.results.left_hand_landmarks
            # print(myHolistic.landmark)
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*(w+h)/2)
                # print(id, cx, cy)
                # print(cz)
                xList.append(cx)
                yList.append(cy)
                self.left_hand_lmList.append([id, cx, cy, cz])

        return self.left_hand_lmList

    def findRighthandLandmark(self, img, draw=True):
        xList = []
        yList = []

        self.right_hand_lmList = []
        if self.results.right_hand_landmarks:
            myHolistic = self.results.right_hand_landmarks
            # print(myHolistic.landmark)
            # print(type(myHolistic.landmark))
            for id, lm in enumerate(myHolistic.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*(w+h)/2)
                # print(id, cx, cy)
                # print(cz)
                xList.append(cx)
                yList.append(cy)
                self.right_hand_lmList.append([id, cx, cy, cz])

        return self.right_hand_lmList

    def left_hand_fingersUp(self):
        fingers = []
        
        if self.left_hand_lmList[self.tipIds[0]][1] < self.left_hand_lmList[self.tipIds[4]][1]:
            if self.left_hand_lmList[self.tipIds[0]][1] < self.left_hand_lmList[self.tipIds[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        if self.left_hand_lmList[self.tipIds[0]][1] > self.left_hand_lmList[self.tipIds[4]][1]:
            if self.left_hand_lmList[self.tipIds[0]][1] > self.left_hand_lmList[self.tipIds[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Fingers except Thumb
        for id in range(1, 5):
            if self.left_hand_lmList[self.tipIds[id]][2] < self.left_hand_lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def right_hand_fingersUp(self):
        fingers = []

        if self.right_hand_lmList[self.tipIds[0]][1] > self.right_hand_lmList[self.tipIds[4]][1]:
            if self.right_hand_lmList[self.tipIds[0]][1] > self.right_hand_lmList[self.tipIds[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        if self.right_hand_lmList[self.tipIds[0]][1] < self.right_hand_lmList[self.tipIds[4]][1]:
            if self.right_hand_lmList[self.tipIds[0]][1] < self.right_hand_lmList[self.tipIds[0] - 2][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Fingers except Thumb
        for id in range(1, 5):
            if self.right_hand_lmList[self.tipIds[id]][2] < self.right_hand_lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def findCenter(self, p1, p2):
        x1, y1 = self.pose_lmList[p1][1:3]
        x2, y2 = self.pose_lmList[p2][1:3]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        return cx, cy

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = p2[0],p2[1]

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255,0,255), t)
            cv2.circle(img, (x1, y1), r, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)

        return length, img

    def findDepth(self, p1, p2):
        depth = abs((self.pose_lmList[p1][3] + self.pose_lmList[p2][3]) / 2)
        return depth

    def findEyeBlink(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255,0,255), t)
            cv2.circle(img, (x1, y1), r, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)

        return length, img

    def findEyeDepth(self, p1, p2):
        depth = abs((self.face_lmList[p1][3] + self.face_lmList[p2][3]) / 2)
        return depth

    def drawLine(self, p1, p2, img, t=3):
        x1, y1 = self.face_lmList[p1][1:3]
        x2, y2 = self.face_lmList[p2][1:3]

        cv2.line(img, (x1, y1), (x2, y2), (255,255,255), t)
