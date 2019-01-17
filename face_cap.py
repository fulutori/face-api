#coding: utf-8
import cv2
import cognitive_face as CF
import requests
import sys
import signal
import os
import requests
from time import sleep
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0'
CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

#顔座標取得
def getRectangle(faceDictionary):
	rect = faceDictionary['faceRectangle']
	left = rect['left']
	top = rect['top']
	right = left + rect['height']
	bottom = top + rect['width']
	return ((left, top), (right, bottom))

#取得結果の描画
def draw(img_url,faces):
	with open(img_url, 'rb') as f:
		binary = f.read()
	img2 = Image.open(BytesIO(binary))
	draw = ImageDraw.Draw(img2)
	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',40)
	for face in faces:
		pos = getRectangle(face)
		text = face['faceAttributes']['gender']+'/'+str(face['faceAttributes']['age'])
		if face['faceAttributes']['gender'] == 'male':
			draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+220,pos[1][1]+40), fill='#fff', outline='#fff')
			#draw.rectangle((pos[0],pos[1]), outline='blue')
			draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='blue')
		elif face['faceAttributes']['gender'] == 'female':
			draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+260,pos[1][1]+40), fill='#fff', outline='#fff')
			#draw.rectangle((pos[0],pos[1]), outline='red')
			draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='red')
	img2.save(img_url, quality=95)

if __name__ == '__main__':
	# 定数定義
	ESC_KEY = 27     # Escキー
	ENTER_KEY = 13	 # Enterキー
	INTERVAL= 33     # 待ち時間
	FRAME_RATE = 30  # fps

	ORG_WINDOW_NAME = "org"
	#GAUSSIAN_WINDOW_NAME = "gaussian"

	DEVICE_ID = 1

	img_url = 'photo.png'
	img_url_pro = 'processing.png'
	im_pro = cv2.imread(img_url_pro)

	# 分類器の指定
	cascade_file = '/usr/local/share/OpenCV/lbpcascades/lbpcascade_frontalface.xml'
	cascade = cv2.CascadeClassifier(cascade_file)

	# カメラ映像取得
	cap = cv2.VideoCapture(DEVICE_ID)

	# 初期フレームの読込
	end_flag, c_frame = cap.read()
	sleep(1)
	height, width, channels = c_frame.shape
	
	# ウィンドウの準備
	cv2.namedWindow(ORG_WINDOW_NAME)
	#cv2.namedWindow(GAUSSIAN_WINDOW_NAME)

	# 変換処理ループ
	while end_flag == True:

		# 画像の取得と顔の検出
		c_frame = cv2.flip(c_frame, 1)
		img = c_frame
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))

		# 検出した顔に印を付ける
		for (x, y, w, h) in face_list:
			color = (0, 0, 225)
			pen_w = 3
			cv2.rectangle(c_frame, (x, y), (x+w, y+h), color, thickness = pen_w)

		# フレーム表示
		#cv2.imshow(ORG_WINDOW_NAME, c_frame)
		#cv2.imshow(GAUSSIAN_WINDOW_NAME, img_gray)

		# Escキーで終了
		key = cv2.waitKey(INTERVAL)
		if key == ESC_KEY:
			break
		elif key == ENTER_KEY:
			cv2.imshow(ORG_WINDOW_NAME, im_pro)
			cv2.waitKey(1)
			cv2.imwrite(img_url, c_frame)
			faces = CF.face.detect(img_url, face_id=True, landmarks=False, attributes='age,gender')
			if len(faces)==0:
				print('顔を認識できませんでした')
			else:
				draw(img_url,faces)
				im = cv2.imread(img_url)
				#cv2.namedwindow('face', cv2.WINDOW_NORMAL)
				cv2.imshow(ORG_WINDOW_NAME, im)
				cv2.waitKey(0)
				#cv2.destroyAllWindows()
				#im = Image.open(img_url)
				#im.show()
		else:
			cv2.imshow(ORG_WINDOW_NAME, c_frame)


		# 次のフレーム読み込み
		end_flag, c_frame = cap.read()

	# 終了処理
	cv2.destroyAllWindows()
	cap.release()
