# /usr/bin/env. python

import time
import pygame
import sys
import pygame.camera
from pygame.locals import *
import os
import cv2
import math
import argparse
import numpy as np
import ctypes
import requests
import json


elapsed_time = 0

url_addUser = 'http://39.116.14.193:8080/api/addUser'
url_order = 'http://39.116.14.193:8080/api/order'
url_ranking = 'http://39.116.14.193:8080/api/ranking'

flag_v = ''
order = []
order_list = []
y_cnt = 0
flag_next = 0
flag_back = 0
flag_rank = 0
max_stuff = 0

price_num = 1000
now_price_num = 0

## 초당 프레임 단위 설정 ##
FPS = 60
FramePerSec = pygame.time.Clock()

## 컬러 세팅 ##
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

age = []
gender = []

pos_x = 400
pos_y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '0'
### window 창 위치 옮기기

pygame.init()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen = pygame.display.set_mode(screensize, FULLSCREEN)
# screen = pygame.display.set_mode((500,500))
screen.fill(WHITE)
pygame.display.set_caption("custom kimbab")
### window 사이즈

start_ticks = 0

bab_img = pygame.image.load('bab.png')
cam_img = pygame.image.load('cam.png')
dan_img = pygame.image.load('dan.png')
ham_img = pygame.image.load('ham.png')
che_img = pygame.image.load('che.png')
mat_img = pygame.image.load('mat.png')
egg_img = pygame.image.load('egg.png')
oi_img = pygame.image.load('oi.png')
ung_img = pygame.image.load('ung.png')
don_img = pygame.image.load('don.png')
dang_img = pygame.image.load('dang.png')

big_cam_img = pygame.image.load('big-cam.png')
big_dan_img = pygame.image.load('big-dan.png')
big_ham_img = pygame.image.load('big-ham.png')
big_che_img = pygame.image.load('big-che.png')
big_mat_img = pygame.image.load('big-mat.png')
big_egg_img = pygame.image.load('big-egg.png')
big_oi_img = pygame.image.load('big-oi.png')
big_ung_img = pygame.image.load('big-ung.png')
big_don_img = pygame.image.load('big-don.png')
big_dang_img = pygame.image.load('big-dang.png')

line_cam_img = pygame.image.load('cam-line.png')
line_dan_img = pygame.image.load('dan-line.png')
line_ham_img = pygame.image.load('ham-line.png')
line_che_img = pygame.image.load('che-line.png')
line_mat_img = pygame.image.load('mat-line.png')
line_egg_img = pygame.image.load('egg-line.png')
line_oi_img = pygame.image.load('oi-line.png')
line_ung_img = pygame.image.load('ung-line.png')
line_don_img = pygame.image.load('don-line.png')
line_dang_img = pygame.image.load('dang-line.png')

m_cam_img = pygame.image.load('cam-m.png')
m_don_img = pygame.image.load('don-m.png')
m_mat_img = pygame.image.load('mat-m.png')
m_ham_img = pygame.image.load('ham-m.png')

menupan_img = pygame.image.load("pan.png")

game_font = pygame.font.Font(None, 40)
price_font = pygame.font.Font(None, 60)

cam_stuff = 0
dan_stuff = 0
dang_stuff = 0
don_stuff = 0
oi_stuff = 0
egg_stuff = 0
ung_stuff = 0
ham_stuff = 0
mat_stuff = 0
che_stuff = 0



# 버튼 클래스
class Button:
    def __init__(self, img, x, y, w, h, img_act, x_act, y_act, name, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if (x + w > mouse[0] > x and y + h > mouse[1] > y) or flag_v == name:
            screen.blit(img_act, (x_act, y_act))
            if click[0] and action != None:
                time.sleep(0.02)
                action()
        else:
            screen.blit(img, (x, y))

# 시작화면에 보이는 랭크 5
def rank_5():
    response = requests.get(url_ranking)
    if response.status_code == 200:
        data = response.json()
        ranking_y = 0
        cnt = 1
        print(data)
        
        for i in data:
            gender = i["gender"] if not None else ""
            time_r = i['time'] if not None else ""
            age = i["age"] if not None else ""
            time_r = str(time_r)
            age_list = list(age)
            for i in age_list:
                if i == '\x00':
                    age = age[:age_list.index(i)]
            
            ranking = game_font.render(str(cnt)+". time: "+time_r+" gender: "+ gender+" age: "+age, True, BLACK)
            screen.blit(ranking, (10, 1000+ranking_y))
            #pygame.display.update()
            ranking_y += 50
            cnt += 1
            if ranking_y >= 250:
               break
            print(f"성별 : {gender}, 시간 : {time_r}, 나이 : {age}")
    else:
        print('fuck')

# 재료 추가하는 함수들
def push_cam():
    global flag_v, now_price_num
    flag_v = 'cam'
    now_price_num = 700
    print("cam")


def push_dan():
    global flag_v, now_price_num
    flag_v = 'dan'
    now_price_num = 500
    print("dan")


def push_ham():
    global flag_v, now_price_num
    flag_v = 'ham'
    now_price_num = 700
    print("ham")


def push_che():
    global flag_v, now_price_num
    flag_v = 'che'
    now_price_num = 500
    print("che")


def push_mat():
    global flag_v, now_price_num
    flag_v = 'mat'
    now_price_num = 700
    print("mat")


def push_egg():
    global flag_v, now_price_num
    flag_v = 'egg'
    now_price_num = 500
    print("egg")


def push_oi():
    global flag_v, now_price_num
    flag_v = 'oi'
    now_price_num = 500
    print("oi")


def push_ung():
    global flag_v, now_price_num
    flag_v = 'ung'
    now_price_num = 500
    print("ung")


def push_don():
    global flag_v, now_price_num
    flag_v = 'don'
    now_price_num = 700
    print("don")


def push_dang():
    global flag_v, now_price_num
    flag_v = 'dang'
    now_price_num = 500
    print("dang")


# 서버에 정보를 보내는 함수
def push_money():
    global order_list, price_num, elapsed_time, gender, age
    global flag_rank
    global url_order, url_addUser
    data_order = {
        "stuff": order_list,
        "price": price_num
    }

    json_data_order = json.dumps(data_order)
    response = requests.post(url_order, data=json_data_order, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("good_order")
    else:
        print("fuck_order")
    data_addUser = {
        "gender": gender,
        "time": elapsed_time,
        "age": age[1:-1]
    }
    json_data_addUser = json.dumps(data_addUser)
    response = requests.post(url_addUser, data=json_data_addUser, headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        print("good_addUser")
    else:
        print("fuck_addUser")

    flag_rank = 1


# 결제 페이지 넘어가는거
def push_next():
    global flag_next
    flag_next = 1

# 다시 start페이지로 가는거임
def push_back():
    global flag_back
    flag_back = 1

# 리셋 버튼 함수
def push_rst():
    global order, order_list, price_num, max_stuff, cam_stuff, che_stuff, dan_stuff, dang_stuff, don_stuff, oi_stuff, ung_stuff, egg_stuff, ham_stuff, mat_stuff
    order_list = []
    order = []
    price_num = 1000
    max_stuff = 0
    cam_stuff = 0
    che_stuff = 0
    dan_stuff = 0
    dang_stuff = 0
    don_stuff = 0
    oi_stuff = 0
    ung_stuff = 0
    egg_stuff = 0
    ham_stuff = 0
    mat_stuff = 0


# 결제 페이지
def money_page():
    global age
    print(price_num)
    global flag_rank, flag_back
    while True:
        screen.fill(WHITE)
        price = price_font.render("price: " + str(price_num), True, BLACK)
        age_list = list(age)
        for i in age:
            if i == '\x00':
                age = age[:age_list.index(i)]
        age_img = price_font.render("age: "+age, True, BLACK)
        time_img = price_font.render("time: "+str(elapsed_time), True, BLACK)
        
        card_img = pygame.image.load("card.png")
        cash_img = pygame.image.load("money.png")
        back_img = pygame.image.load("back.png")
        money_Button = Button(card_img, 200, 200, 500, 500, card_img, 200, 200, 'card', push_money)
        money_Button = Button(cash_img, 200, 700, 500, 500, cash_img, 200, 700, 'cash', push_money)
        back_Button = Button(back_img, 10, 1320, 500, 500, back_img, 10, 1320, 'back', push_back)

        screen.blit(time_img, (10, 10))
        screen.blit(age_img, (350, 10))
        screen.blit(price, (650, 10))
        
        pygame.display.update()
        
        if flag_rank == 1:
            money_Button = Button(card_img, 200, 200, 500, 500, card_img, 200, 200, 'card')
            money_Button = Button(cash_img, 200, 700, 500, 500, cash_img, 200, 700, 'cash')
            rank()
            break
        
        if flag_back == 1:
            back_Button = Button(back_img, 10, 1320, 500, 500, back_img, 10, 1320, 'back')
            start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == ord('q'):
                        sys.exit()

# 밥에 재료들 가져다 박는 로직같음
def push_bab():
    global flag_v
    global order, price_num, now_price_num, max_stuff, cam_stuff, che_stuff, dan_stuff, dang_stuff, don_stuff, oi_stuff, ung_stuff, egg_stuff, ham_stuff, mat_stuff
    
    if max_stuff < 10:
        if flag_v == 'cam':
            if(cam_stuff < 3):
                order.append(line_cam_img)
                cam_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'che':
            if(che_stuff < 3):
                order.append(line_che_img)
                che_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'dan':
            if(dan_stuff < 3):
                order.append(line_dan_img)
                dan_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'ung':
            if(ung_stuff < 3):
                order.append(line_ung_img)
                ung_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'ham':
            if(ham_stuff < 3):
                order.append(line_ham_img)
                ham_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'oi':
            if(oi_stuff < 3):
                order.append(line_oi_img)
                oi_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'don':
            if(don_stuff < 3):
                order.append(line_don_img)
                don_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'mat':
            if(mat_stuff < 3):
                order.append(line_mat_img)
                mat_stuff += 1
                max_stuff += 1
                price_num += now_price_num
        if flag_v == 'dang':
            if(dang_stuff < 3):
                order.append(line_dang_img)
                max_stuff += 1
                dang_stuff += 1
                price_num += now_price_num
        if flag_v == 'egg':
            if(egg_stuff < 3):
                order.append(line_egg_img)
                max_stuff += 1
                egg_stuff += 1
                price_num += now_price_num
    order_list.append(flag_v)

# 랭킹 쪽 부분
def rank():
    global url_ranking, flag_next, flag_rank
    global order, order_list, price_num, now_price_num, flag_v
    order = []
    order_list = []
    price_num = 1000
    now_price_num = 0
    flag_next = 0
    flag_rank = 0
    flag_v = ''

    response = requests.get(url_ranking)
    if response.status_code == 200:
        data = response.json()
        ranking_y = 0
        cnt = 1
        print(data)
        screen.fill(WHITE)
        for i in data:
            gender = i["gender"] if not None else ""
            time_r = i['time'] if not None else ""
            age = i["age"] if not None else ""
            time_r = str(time_r)
            age_list = list(age)
            for i in age_list:
                if i == '\x00':
                    age = age[:age_list.index(i)]
            
            ranking = game_font.render(str(cnt)+".    time: "+time_r+"         gender: "+ gender+"         age: "+age, True, BLACK)
            screen.blit(ranking, (10, 10+ranking_y))
            pygame.display.update()
            ranking_y += 50
            cnt += 1
            if ranking_y >= 1000:
               break
    else:
        print('fuck')
    for i in range(0,7):
        cnt_time = price_font.render('time: '+str(7-i), True, BLACK)
        cnt_time_cls = price_font.render('time: '+str(8-i), True, WHITE)
    
        screen.blit(cnt_time_cls, (10,1400))
        screen.blit(cnt_time, (10, 1400))
        pygame.display.update()
        time.sleep(1)


# 김밥 만드는 곳
def start():
    global flag_next, flag_start, max_stuff
    global elapsed_time, start_ticks
    print(gender)
    print(age[1:-1])
    doma_img = pygame.image.load('doma.jpg')
    start_ticks = pygame.time.get_ticks()
    while True:
        screen.blit(doma_img, (0, 0))
        # 경과 시간 계산
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        format(elapsed_time, ".1f")

        # 타이머
        timer = price_font.render("timer: " + str(elapsed_time), True, WHITE)
        total_price = price_font.render("total price: "+str(price_num), True, WHITE)
    
        screen.blit(menupan_img, (50,1400))
        next_img = pygame.image.load("next.png")
        rst_img = pygame.image.load("reset.png")

        # 경과 시간 표시
        screen.blit(total_price, (10,10))
        screen.blit(timer, (650, 10))

        max_stuff_message = price_font.render('max stuff!', True, WHITE)
        now_stuff_message = price_font.render('now stuff: ' +str(max_stuff), True, WHITE)
        
        # 최대 재료가 찼을 때
        if(max_stuff < 10):
            screen.blit(now_stuff_message, (380, 10))
        if(max_stuff >= 10):
            screen.blit(max_stuff_message, (400, 10))


        # 재료 버튼들
        bab_button = Button(bab_img, 10, 500, 500, 500, bab_img, 10, 500, 'bab', push_bab)
        cam_button = Button(cam_img, 0, 50, 250, 250, big_cam_img, 0, 50, 'cam', push_cam)
        dan_button = Button(dan_img, 300, 50, 250, 250, big_dan_img, 300, 50, 'dan', push_dan)
        ham_button = Button(ham_img, 600, 50, 250, 250, big_ham_img, 600, 50, 'ham', push_ham)
        che_button = Button(che_img, 0, 250, 250, 250, big_che_img, 0, 250, 'che', push_che)
        mat_button = Button(mat_img, 300, 250, 250, 250, big_mat_img, 300, 250, 'mat', push_mat)
        egg_button = Button(egg_img, 600, 250, 250, 250, big_egg_img, 600, 250, 'egg', push_egg)
        oi_button = Button(oi_img, 600, 450, 250, 250, big_oi_img, 600, 450, 'oi', push_oi)
        ung_button = Button(ung_img, 600, 650, 250, 250, big_ung_img, 600, 650, 'ung', push_ung)
        don_button = Button(don_img, 600, 850, 250, 250, big_don_img, 600, 850, 'don', push_don)
        dang_button = Button(dang_img, 600, 1050, 250, 250, big_dang_img, 600, 1050, 'dang', push_dang)
        next_button = Button(next_img, 630, 1300, 250, 250, next_img, 630, 1300, 'next', push_next)
        rst_button = Button(rst_img, 430, 1300, 250, 250, rst_img, 430, 1300, 'rst', push_rst)


        # 재료 클릭시
        if flag_next == 1:
            print("next!")
            flag_start = 0
            bab_button = Button(bab_img, 10, 500, 500, 500, bab_img, 10, 500, 'bab')
            cam_button = Button(cam_img, 0, 50, 250, 250, big_cam_img, 0, 50, 'cam')
            dan_button = Button(dan_img, 300, 50, 250, 250, big_dan_img, 300, 50, 'dan')
            ham_button = Button(ham_img, 600, 50, 250, 250, big_ham_img, 600, 50, 'ham')
            che_button = Button(che_img, 0, 250, 250, 250, big_che_img, 0, 250, 'che')
            mat_button = Button(mat_img, 300, 250, 250, 250, big_mat_img, 300, 250, 'mat')
            egg_button = Button(egg_img, 600, 250, 250, 250, big_egg_img, 600, 250, 'egg')
            oi_button = Button(oi_img, 600, 450, 250, 250, big_oi_img, 600, 450, 'oi')
            ung_button = Button(ung_img, 600, 650, 250, 250, big_ung_img, 600, 650, 'ung')
            don_button = Button(don_img, 600, 850, 250, 250, big_don_img, 600, 850, 'don')
            dang_button = Button(dang_img, 600, 1050, 250, 250, big_dang_img, 600, 1050, 'dang')
            next_button = Button(next_img, 630, 1300, 250, 250, next_img, 630, 1300, 'next')
            rst_button = Button(rst_img, 430, 1300, 250, 250, rst_img, 430, 1300, 'rst')
                
            money_page()
            break

        # 재료 추가 같음
        global order
        global y_cnt
        y_cnt = 0
        for i in order:
            screen.blit(i, (10, 600 + y_cnt))
            y_cnt += 25
            if y_cnt >= 600:
                y_cnt = 10

        # 추천메뉴
        if gender == 'Male':
            if age == '(0-2)':
                screen.blit(m_ham_img, (180,1400))
                screen.blit(m_mat_img, (280,1400))
            elif age == '(4-6)':
                screen.blit(m_mat_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
            elif age == '(8-12)':
                screen.blit(m_cam_img, (180,1400))
                screen.blit(m_ham_img, (280,1400))
            elif age == '(15-20)':
                screen.blit(m_don_img, (180,1400))
                screen.blit(m_ham_img, (280,1400))
            elif age == '(25-32)':
                screen.blit(m_don_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
            elif age == '(38-43)':
                screen.blit(m_don_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
            elif age == '(48-53)':
                screen.blit(m_mat_img, (180,1400))
                screen.blit(m_don_img, (280,1400))
            else:
                screen.blit(m_mat_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
        else:
            if age == '(0-2)':
                screen.blit(m_ham_img, (180,1400))
                screen.blit(m_mat_img, (280,1400))
            elif age == '(4-6)':
                screen.blit(m_mat_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
            elif age == '(8-12)':
                screen.blit(m_cam_img, (180,1400))
                screen.blit(m_ham_img, (280,1400))
            elif age == '(15-20)':
                screen.blit(m_don_img, (180,1400))
                screen.blit(m_ham_img, (280,1400))
            elif age == '(25-32)':
                screen.blit(m_don_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
            elif age == '(38-43)':
                screen.blit(m_don_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
            elif age == '(48-53)':
                screen.blit(m_mat_img, (180,1400))
                screen.blit(m_don_img, (280,1400))
            else:
                screen.blit(m_mat_img, (180,1400))
                screen.blit(m_cam_img, (280,1400))
                
        
        # 뭔지 모르는데 그냥 파이게임띄워주는 거인듯
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == ord('q'):
                    sys.exit()


# 얼굴 인식 네모
def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (100, 100), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), WHITE, int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes

# 얼굴 인식 AI
parser = argparse.ArgumentParser()
parser.add_argument('--image')

args = parser.parse_args()

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

video = cv2.VideoCapture(0)

padding = 20
pygame.display.update()
while 1:
    FramePerSec.tick(FPS)
    hasFrame, frame = video.read()

    # image = cam.get_image()
    # new_image = pygame.transform.flip(image, True, False)
    ##좌우 반전
    # screen.blit(new_image,(0,0))
    # pygame.display.flip()
    # pygame.display.update()

    resultImg, faceBoxes = highlightFace(faceNet, frame)
    if not faceBoxes:
        flag_start = 0
        print("No face detected")
    else:
        flag_start = 1

    for faceBox in faceBoxes:
        face = frame[max(0, faceBox[1] - padding):
                     min(faceBox[3] + padding, frame.shape[0] - 1), max(0, faceBox[0] - padding)
                                                                    :min(faceBox[2] + padding, frame.shape[1] - 1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        print(f'Gender: {gender}')

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        print(f'Age: {age[1:-1]} years')
        cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 255), 2, cv2.LINE_AA)
    screen.fill(WHITE)
    cv2.imwrite('test.jpg', resultImg)
    rank_5()
    if flag_start == 1:
        start()
    else:
        bg = pygame.image.load('test.jpg')
        screen.blit(bg, (0, 0))
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == ord('q'):
                sys.exit()
        if event.type == pygame.QUIT:
            sys.exit()
    if not hasFrame:
        cv2.waitKey()
        break
