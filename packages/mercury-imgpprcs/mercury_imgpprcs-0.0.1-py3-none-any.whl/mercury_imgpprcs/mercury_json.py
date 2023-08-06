import json
import os
import platform as pf
import re
import sys

import cv2
import requests

from . import json_filter

URL = 'https://mercurypreprcs.com/filters/'


class Filters:

    def __init__(self, apikey):
        self.__apikey = apikey  # 객체 생성시 apikey를 입력받는다
        self.__imgNames = []
        self.__imgs = []

    def img_processing(self, imgpath, filterInfo, savepath=None):

        if not os.path.exists(imgpath):
            print('\033[96m' + '[MERCURY] 이미지 파일(jpg, jpeg, png) 또는 폴더의 경로를 입력해 주세요' + '\033[0m')
            return
        elif os.path.isfile(imgpath):
            if imgpath.lower().endswith(('.jpg', '.jpeg', '.png')):
                self.__imgNames.append(re.split('\\\\|/', imgpath)[-1])
                img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
                self.__imgs.append(img)
            else:
                print('\033[96m' + '[MERCURY] 지원되지 않는 이미지입니다 (jpg, jpeg, png 가능)' + '\033[0m')
                return
        elif os.path.isdir(imgpath):
            self.__imgNames = [_ for _ in os.listdir(imgpath) if _.lower().endswith(('.jpg', '.jpeg', '.png'))]

            if len(self.__imgNames) == 0:
                print('\033[96m' + '[MERCURY] 지원 가능한 이미지가 없습니다 (jpg, jpeg, png 가능)' + '\033[0m')
                return

            self.__imgs = [cv2.imread(os.path.join(imgpath, _), cv2.IMREAD_COLOR) for _ in os.listdir(imgpath)
                           if _.lower().endswith(('.jpg', '.jpeg', '.png'))]

        try:
            req_cnt = len(self.__imgs)

            file = {}
            if os.path.isfile(imgpath):
                file['file'] = open(imgpath, 'rb')
            elif os.path.isdir(imgpath):
                file['file'] = open(os.path.join(imgpath, self.__imgNames[0]), 'rb')

            f_cnt = len(filterInfo.keys())

            f_nms = list(filterInfo.keys())

            f_prms = filterInfo

            osInfo = pf.platform()  # 사용자의 운영체제 정보

            approach = "A"

            call = "J"

            data = {
                "apikey": self.__apikey,
                "req_cnt": req_cnt,
                "f_cnt": f_cnt,
                "f_nms": str(f_nms),
                "f_prms": str(f_prms),
                "os": osInfo,
                "approach": approach,
                "call": call
            }

            response = requests.post(URL, data=data, files=file)

            content_str = response.content.decode('utf-8')
            content_json = json.loads(content_str)

            if content_json['msg'] == 'error':
                print('\033[96m' + '[MERCURY] ' + content_json['errorMsg'] + '\033[0m')
                return

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        try:
            for filterName, params in filterInfo.items():
                self.__imgs = getattr(sys.modules['mercury_imgpprcs.json_filter'], filterName)(self.__imgs, params)
        except AttributeError as e:
            print('\033[96m' + '[MERCURY] \'' + filterName + '\' 필터는 제공되지 않는 필터입니다\033[0m')
            return
        except KeyError as e:
            print('\033[96m' + '[MERCURY] \'' + filterName + '\' 필터의 ' + str(e) + ' 파라미터 값이 없습니다\033[0m')
            return

        if savepath is None:
            return self.__imgs
        else:
            if not (savepath[-1:] == '\\' or savepath[-1:] == '/'):
                savepath += '/'

            if not os.path.exists(savepath):
                os.makedirs(savepath)

            for i in range(len(self.__imgs)):
                cv2.imwrite(savepath + 'm_' + self.__imgNames[i], self.__imgs[i])
