#coding: utf-8
import cv2
import cognitive_face as CF
import requests
import sys
import signal
import os
import requests
import random
import datetime
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

def draw_t(img_url,save_url,faces):
	with open(img_url, 'rb') as f:
		binary = f.read()
	img2 = Image.open(BytesIO(binary))
	draw = ImageDraw.Draw(img2)
	font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf',20)
	for face in faces:
		pos = getRectangle(face)
		text = face['faceAttributes']['gender']+'/'+str(face['faceAttributes']['age'])
		if face['faceAttributes']['gender'] == 'male':
			draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+135,pos[1][1]+20), fill='#fff', outline='#fff')
			draw.rectangle((pos[0],pos[1]), outline='blue')
			draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='blue')
		elif face['faceAttributes']['gender'] == 'female':
			draw.rectangle((pos[0][0],pos[1][1],pos[0][0]+155,pos[1][1]+20), fill='#fff', outline='#fff')
			draw.rectangle((pos[0],pos[1]), outline='red')
			draw.text((pos[0][0]+2,pos[1][1]+2), text, font=font, fill='red')
	img2.save(save_url, quality=100)

if __name__ == '__main__':
	dir_list = ["./face01/","./face02/","./face03/","./face04/"]
	for dir_name in dir_list:
		files = os.listdir(dir_name)
		files.sort()
		dir_name_api = dir_name.replace("./","./api_")
		for f in files:
			img_url = dir_name+f
			faces = CF.face.detect(img_url, face_id=True, landmarks=False, attributes='age,gender')
			save_url = dir_name_api+f
			if len(faces)==0:
				with open(img_url, 'rb') as bf:
					binary = bf.read()
					img = Image.open(BytesIO(binary))
					draw_f = ImageDraw.Draw(img)
					img.save(save_url, quality=100)
			else:
				try:
					draw_t(img_url,save_url,faces)
					print("ok: "+save_url)
				except:
					print("out: "+img_url)
			sleep(7)
	api_list = ["./api_face01/","./api_face02/","./api_face03/","./api_face04/"]
	for dir_name in api_list:
		files = os.listdir(dir_name)
		files.sort()
		fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
		video_name = dir_name.replace("./api_","").replace("/","")+".mp4"
		video = cv2.VideoWriter(video_name, fourcc, 20.0, (640, 480))
		for f in files:
			img = cv2.imread(f)
			video.write(img)
		video.release()

