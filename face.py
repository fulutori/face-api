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

def getRectangle(faceDictionary):
	rect = faceDictionary['faceRectangle']
	left = rect['left']
	top = rect['top']
	right = left + rect['height']
	bottom = top + rect['width']
	return ((left, top), (right, bottom))

def draw(img_url,faces):
	with open(img_url, 'rb') as f:
		binary = f.read()
	img = Image.open(BytesIO(binary))
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',20)
	for face in faces:
		pos = getRectangle(face)
		text = face['faceAttributes']['gender']+'/'+str(face['faceAttributes']['age'])
		if len(faces) == 1:
			if face['faceAttributes']['gender'] == 'male':
				draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+110,pos[1][1]+20), fill='#fff', outline='#fff')
				draw.rectangle((pos[0],pos[1]), outline='blue')
				draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='blue')
			elif face['faceAttributes']['gender'] == 'female':
				draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+130,pos[1][1]+20), fill='#fff', outline='#fff')
				draw.rectangle((pos[0],pos[1]), outline='red')
				draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='red')
	img.save(img_url.replace('.jpg','_face-api.jpg').replace('img/','face/'), quality=95)

if __name__ == "__main__":
	dir_path = input('>> ')
	files = os.listdir(dir_path)
	for file in files:
		img_url = "img/"+file
		faces = CF.face.detect(img_url, face_id=True, landmarks=False, attributes='age,gender')
		if len(faces)==0:
			print('顔を認識できませんでした')
		else:
			draw(img_url,faces)
		print(file)
		sleep(4)