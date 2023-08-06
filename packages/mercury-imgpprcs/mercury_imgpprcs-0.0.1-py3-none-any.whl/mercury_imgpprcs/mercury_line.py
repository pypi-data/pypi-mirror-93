import base64
import json
import os
import platform as pf
import sys

import cv2
import numpy as np
import requests

from . import line_filter

URL = 'https://mercurypreprcs.com/filters/'


class Filters:

    # 초기화
    def __init__(self, apikey):
        self.__apikey = apikey
        self.__moduleName = 'mercury_imgpprcs.line_filter'

    def __typeCheck(self, imgs):

        if type(imgs) is str:
            return 'imgPath'
        elif type(imgs) is np.ndarray:
            return 'imgArr'
        elif type(imgs) is list:
            return 'imgArrList'

    def __readImg(self, imgpath):

        imgs = []

        if not os.path.exists(imgpath):
            print('\033[96m' + '[MERCURY] 이미지 파일(jpg, jpeg, png) 또는 폴더의 경로를 입력해 주세요' + '\033[0m')
            return imgs
        elif os.path.isfile(imgpath):
            if imgpath.lower().endswith(('.jpg', '.jpeg', '.png')):
                img = cv2.imread(imgpath, cv2.IMREAD_COLOR)
                imgs.append(img)
                return imgs
            else:
                print('\033[96m' + '[MERCURY] 지원되지 않는 이미지입니다 (jpg, jpeg, png 가능)' + '\033[0m')
                return imgs
        elif os.path.isdir(imgpath):
            imgs = [cv2.imread(os.path.join(imgpath, _), cv2.IMREAD_COLOR) for _ in os.listdir(imgpath)
                    if _.lower().endswith(('.jpg', '.jpeg', '.png'))]

            if len(imgs) == 0:
                print('\033[96m' + '[MERCURY] 지원 가능한 이미지가 없습니다 (jpg, jpeg, png 가능)' + '\033[0m')
                return imgs

            return imgs


    def saveImg(self, imgs, savepath, ext='jpg', text=None):
        basic_ext = ['jpg', 'jpeg', 'png']
        if self.__typeCheck(imgs) == 'imgArr':
            if ext in basic_ext:
                if text is not None:
                    cv2.imwrite(savepath + text + '.' + ext, imgs)
                else:
                    cv2.imwrite(savepath + 'mercury.' + ext, imgs)
        elif self.__typeCheck(imgs) == 'imgArrList':
            if ext in basic_ext:
                if text is not None:
                    for i in range(len(imgs)):
                        cv2.imwrite(savepath + text + '_' + str(i) + '.' + ext, imgs[i])
                else:
                    for i in range(len(imgs)):
                        cv2.imwrite(savepath + 'mercury_' + str(i) + '.' + ext, imgs[i])

    def __saveLog(self, imgs, f_nm, params):
        try:
            req_cnt = len(imgs)

            file = {}
            _, img_arr = cv2.imencode('.jpg', imgs[0])
            im_bytes = img_arr.tobytes()
            file['file'] = im_bytes

            f_cnt = 1

            f_nms = [f_nm]

            f_prms = {
                f_nm: params
            }

            osInfo = pf.platform()

            approach = "A"

            call = "L"

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
                raise SystemExit(0)

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def __callDef(self, defName, img, params):

        try:
            return getattr(sys.modules[self.__moduleName], defName)(img, params)
        except AttributeError as e:
            print('\033[96m' + '[MERCURY] \'' + defName + '\' 필터는 제공되지 않는 필터입니다\033[0m')
            sys.exit()
        except KeyError as e:
            print('\033[96m' + '[MERCURY] \'' + defName + '\' 필터의 ' + str(e) + ' 파라미터 값이 없습니다\033[0m')
            sys.exit()

    def __prprcsByImgType(self, defName, img, params):

        if self.__typeCheck(img) == 'imgPath':

            imgs = self.__readImg(img)

            self.__saveLog(imgs, defName, params)

            for i in range(len(imgs)):
                imgs[i] = self.__callDef(defName, imgs[i], params)

            return imgs

        elif self.__typeCheck(img) == 'imgArr':

            img = self.__callDef(defName, img, params)

            imgarr = [img]

            self.__saveLog(imgarr, defName, params)

            return imgarr

        elif self.__typeCheck(img) == 'imgArrList':

            # 로그 남기고 전처리 진행
            self.__saveLog(img, defName, params)

            for i in range(len(img)):
                img[i] = self.__callDef(defName, img[i], params)

            return img

    ############################################ Binarization

    def threshold_binary(self, imgs, thresh, maxvalue):

        params = {
            'thresh': thresh,
            'maxvalue': maxvalue,
        }

        return self.__prprcsByImgType('threshold_binary', imgs, params)

    def threshold_binary_inverse(self, imgs, thresh, maxvalue):

        params = {
            'thresh': thresh,
            'maxvalue': maxvalue,
        }

        return self.__prprcsByImgType('threshold_binary_inverse', imgs, params)

    def threshold_truncate(self, imgs, thresh):

        params = {
            'thresh': thresh,
        }

        return self.__prprcsByImgType('threshold_truncate', imgs, params)

    def threshold_tozero(self, imgs, thresh):

        params = {
            'thresh': thresh,
        }

        return self.__prprcsByImgType('threshold_tozero', imgs, params)

    def threshold_tozero_inverse(self, imgs, thresh):

        params = {
            'thresh': thresh,
        }

        return self.__prprcsByImgType('threshold_tozero_inverse', imgs, params)

    def threshold_triangle(self, imgs, maxvalue):

        params = {
            'maxvalue': maxvalue,
        }

        return self.__prprcsByImgType('threshold_triangle', imgs, params)

    def threshold_otsu(self, imgs, maxvalue):

        params = {
            'maxvalue': maxvalue,
        }

        return self.__prprcsByImgType('threshold_otsu', imgs, params)

    def adaptive_threshold_gaussian_c(self, imgs, maxvalue, block_size, c):

        params = {
            'maxvalue': maxvalue,
            'block_size': block_size,
            'c': c,
        }

        return self.__prprcsByImgType('adaptive_threshold_gaussian_c', imgs, params)

    def adaptive_threshold_mean_c(self, imgs, maxvalue, block_size, c):

        params = {
            'maxvalue': maxvalue,
            'block_size': block_size,
            'c': c,
        }

        return self.__prprcsByImgType('adaptive_threshold_mean_c', imgs, params)

    ############################################ Colormodel

    def grayscale(self, imgs):

        params = {}

        return self.__prprcsByImgType('grayscale', imgs, params)

    def hsv(self, imgs):

        params = {}

        return self.__prprcsByImgType('hsv', imgs, params)

    ############################################ Edge

    def basic_gradient_kernel(self, imgs):

        params = {}

        return self.__prprcsByImgType('basic_gradient_kernel', imgs, params)

    def canny(self, imgs, threshold1, threshold2):

        params = {
            'threshold1': threshold1,
            'threshold2': threshold2,
        }

        return self.__prprcsByImgType('canny', imgs, params)

    def difference_of_gaussian(self, imgs, ksize_1, sigmaX_1, sigmaY_1, ksize_2, sigmaX_2, sigmaY_2):

        params = {
            'ksize_1': ksize_1,
            'sigmaX_1': sigmaX_1,
            'sigmaY_1': sigmaY_1,
            'ksize_2': ksize_2,
            'sigmaX_2': sigmaX_2,
            'sigmaY_2': sigmaY_2,
        }

        return self.__prprcsByImgType('difference_of_gaussian', imgs, params)

    def emboss(self, imgs):

        params = {}

        return self.__prprcsByImgType('emboss', imgs, params)

    def gabor(self, imgs, ksize, sigma, theta, lambd, gamma, psi):

        params = {
            'ksize': ksize,
            'sigma': sigma,
            'theta': theta,
            'lambd': lambd,
            'gamma': gamma,
            'psi': psi,
        }

        return self.__prprcsByImgType('gabor', imgs, params)

    def high_pass(self, imgs):

        params = {}

        return self.__prprcsByImgType('high_pass', imgs, params)

    def laplacian(self, imgs, ksize, scale, delta):

        params = {
            'ksize': ksize,
            'scale': scale,
            'delta': delta,
        }

        return self.__prprcsByImgType('laplacian', imgs, params)

    def laplacian_of_gaussian(self, imgs, g_ksize, g_sigmaX, g_sigmaY, ksize, scale, delta):

        params = {
            'g_ksize': g_ksize,
            'g_sigmaX': g_sigmaX,
            'g_sigmaY': g_sigmaY,
            'ksize': ksize,
            'scale': scale,
            'delta': delta,
        }

        return self.__prprcsByImgType('laplacian_of_gaussian', imgs, params)

    def prewitt(self, imgs, alpha, beta, gamma):

        params = {
            'alpha': alpha,
            'beta': beta,
            'gamma': gamma,
        }

        return self.__prprcsByImgType('prewitt', imgs, params)

    def roberts(self, imgs, alpha, beta, gamma):

        params = {
            'alpha': alpha,
            'beta': beta,
            'gamma': gamma,
        }

        return self.__prprcsByImgType('roberts', imgs, params)

    def scharr(self, imgs):

        params = {}

        return self.__prprcsByImgType('scharr', imgs, params)

    def sobel(self, imgs, ksize, scale):

        params = {
            'ksize': ksize,
            'scale': scale,
        }

        return self.__prprcsByImgType('sobel', imgs, params)

    ############################################ Morphology

    def blackhat(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('blackhat', imgs, params)

    def closing(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('closing', imgs, params)

    def dilation(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('dilation', imgs, params)

    def erosion(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('erosion', imgs, params)

    def gradient(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('gradient', imgs, params)

    def opening(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('opening', imgs, params)

    def tophat(self, imgs, ksize, iterations):

        params = {
            'ksize': ksize,
            'iterations': iterations,
        }

        return self.__prprcsByImgType('tophat', imgs, params)

    ############################################ Smoothing

    def averaging(self, imgs, ksize):

        params = {
            'ksize': ksize,
        }

        return self.__prprcsByImgType('averaging', imgs, params)

    def bilateral(self, imgs, d, sigma_color, sigma_space):

        params = {
            'd': d,
            'sigma_color': sigma_color,
            'sigma_space': sigma_space,
        }

        return self.__prprcsByImgType('bilateral', imgs, params)

    def gaussian(self, imgs, ksize, sigmaX, sigmaY):

        params = {
            'ksize': ksize,
            'sigmaX': sigmaX,
            'sigmaY': sigmaY,
        }

        return self.__prprcsByImgType('gaussian', imgs, params)

    def median(self, imgs, ksize):

        params = {
            'ksize': ksize,
        }

        return self.__prprcsByImgType('median', imgs, params)

    def motion_smoothing(self, imgs, ksize):

        params = {
            'ksize': ksize,
        }

        return self.__prprcsByImgType('motion_smoothing', imgs, params)

    def radial_smoothing(self, imgs, iterations):

        params = {
            'iterations': iterations,
        }

        return self.__prprcsByImgType('radial_smoothing', imgs, params)

    def watercolor(self, imgs, d, sigma_color, sigma_space, iterate):

        params = {
            'd': d,
            'sigma_color': sigma_color,
            'sigma_space': sigma_space,
            'iterate': iterate,
        }

        return self.__prprcsByImgType('watercolor', imgs, params)

    ############################################ Sharpening

    def sharpen(self, imgs, alpha):

        params = {
            'alpha': alpha,
        }

        return self.__prprcsByImgType('sharpen', imgs, params)

    def unsharp(self, imgs, gksize, sigmaX, sigmaY, weight, gamma):

        params = {
            'gksize': gksize,
            'sigmaX': sigmaX,
            'sigmaY': sigmaY,
            'weight': weight,
            'gamma': gamma,
        }

        return self.__prprcsByImgType('unsharp', imgs, params)

    def SSR(self, imgs, ksize):

        params = {
            'ksize': ksize,
        }

        return self.__prprcsByImgType('SSR', imgs, params)

    def MSR(self, imgs):

        params = {}

        return self.__prprcsByImgType('MSR', imgs, params)

    def MSRCR(self, imgs):

        params = {}

        return self.__prprcsByImgType('MSRCR', imgs, params)

    def MSRCP(self, imgs):

        params = {}

        return self.__prprcsByImgType('MSRCP', imgs, params)

    ############################################ Contrast

    def clahe(self, imgs, alpha, ksize):

        params = {
            'alpha': alpha,
            'ksize': ksize,
        }

        return self.__prprcsByImgType('clahe', imgs, params)

    def gamma_correction(self, imgs, gamma):

        params = {
            'gamma': gamma,
        }

        return self.__prprcsByImgType('gamma_correction', imgs, params)

    def histogram_equalization(self, imgs):

        params = {}

        return self.__prprcsByImgType('histogram_equalization', imgs, params)

    def histogram_equalization_color(self, imgs):

        params = {}

        return self.__prprcsByImgType('histogram_equalization_color', imgs, params)

    def logarithmic_transform(self, imgs):

        params = {}

        return self.__prprcsByImgType('logarithmic_transform', imgs, params)

    def saturation_intensity_correction(self, imgs, alpha):

        params = {
            'alpha': alpha,
        }

        return self.__prprcsByImgType('saturation_intensity_correction', imgs, params)

    ############################################ Corner Detection

    def BRIEF(self, imgs):

        params = {}

        return self.__prprcsByImgType('BRIEF', imgs, params)

    def FAST(self, imgs, threshold):

        params = {
            'threshold': threshold,
        }

        return self.__prprcsByImgType('FAST', imgs, params)

    def harris(self, imgs, blocksize, ksize, k):

        params = {
            'blocksize': blocksize,
            'ksize': ksize,
            'k': k,
        }

        return self.__prprcsByImgType('harris', imgs, params)

    def harris_advanced(self, imgs, blocksize, ksize, k):

        params = {
            'blocksize': blocksize,
            'ksize': ksize,
            'k': k,
        }

        return self.__prprcsByImgType('harris_advanced', imgs, params)

    def LBP(self, imgs):

        params = {}

        return self.__prprcsByImgType('LBP', imgs, params)

    def MSER(self, imgs):

        params = {}

        return self.__prprcsByImgType('MSER', imgs, params)

    def ORB(self, imgs):

        params = {}

        return self.__prprcsByImgType('ORB', imgs, params)

    def shi_tomasi(self, imgs, maxcorners, qualitylevel, mindistance):

        params = {
            'maxcorners': maxcorners,
            'qualitylevel': qualitylevel,
            'mindistance': mindistance,
        }

        return self.__prprcsByImgType('shi_tomasi', imgs, params)

    def SIFT(self, imgs):

        params = {}

        return self.__prprcsByImgType('SIFT', imgs, params)
