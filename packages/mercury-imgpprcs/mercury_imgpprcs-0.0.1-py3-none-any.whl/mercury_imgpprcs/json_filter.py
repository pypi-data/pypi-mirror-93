import math

import numpy as np
import cv2

# 전처리될 필터 모음
############################################ Binarization

def threshold_binary(imgs, params):
    thresh = params['thresh']
    maxval = params['maxval']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=thresh, maxval=maxval, type=cv2.THRESH_BINARY)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def threshold_binary_inverse(imgs, params):
    thresh = params['thresh']
    maxval = params['maxval']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=thresh, maxval=maxval, type=cv2.THRESH_BINARY_INV)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def threshold_truncate(imgs, params):
    thresh = params['thresh']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=thresh, maxval=0, type=cv2.THRESH_TRUNC)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def threshold_tozero(imgs, params):
    thresh = params['thresh']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=thresh, maxval=0, type=cv2.THRESH_TOZERO)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def threshold_tozero_inverse(imgs, params):
    thresh = params['thresh']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=thresh, maxval=0, type=cv2.THRESH_TOZERO_INV)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def threshold_triangle(imgs, params):
    maxval = params['maxval']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=0, maxval=maxval, type=cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def threshold_otsu(imgs, params):
    maxval = params['maxval']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        ret, temp = cv2.threshold(temp, thresh=0, maxval=maxval, type=cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def adaptive_threshold_gaussian_c(imgs, params):
    maxval = params['maxval']
    block_size = params['block_size']
    c = params['c']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.adaptiveThreshold(temp, maxValue=maxval, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     thresholdType=cv2.THRESH_BINARY, blockSize=block_size, C=c)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def adaptive_threshold_mean_c(imgs, params):
    maxval = params['maxval']
    block_size = params['block_size']
    c = params['c']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.adaptiveThreshold(temp, maxValue=maxval, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                     thresholdType=cv2.THRESH_BINARY, blockSize=block_size, C=c)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

############################################ Colormodel
def grayscale(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def hsv(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2HSV)
        imgs[i] = temp

    return imgs

############################################ Edge
def basic_gradient_kernel(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        gx_kernel = np.array([[-1, 1]])
        gy_kernel = np.array([[-1], [1]])
        edge_gx = cv2.filter2D(temp, -1, gx_kernel)
        edge_gy = cv2.filter2D(temp, -1, gy_kernel)
        basic = edge_gx + edge_gy
        temp = cv2.cvtColor(basic, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def canny(imgs, params):
    threshold1 = params['threshold1']
    threshold2 = params['threshold2']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.Canny(temp, threshold1=threshold1, threshold2=threshold2)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def difference_of_gaussian(imgs, params):
    ksize_1 = params['ksize_1']
    sigmaX_1 = params['sigmaX_1']
    sigmaY_1 = params['sigmaY_1']
    ksize_2 = params['ksize_2']
    sigmaX_2 = params['sigmaX_2']
    sigmaY_2 = params['sigmaY_2']

    for i in range(len(imgs)):
        temp = imgs[i]
        low = cv2.GaussianBlur(temp, ksize=(ksize_1, ksize_1), sigmaX=sigmaX_1, sigmaY=sigmaY_1)
        high = cv2.GaussianBlur(temp, ksize=(ksize_2, ksize_2), sigmaX=sigmaX_2, sigmaY=sigmaY_2)
        low_gray = cv2.cvtColor(low, cv2.COLOR_RGB2GRAY)
        high_gray = cv2.cvtColor(high, cv2.COLOR_RGB2GRAY)
        temp = low_gray - high_gray
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def emboss(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel_emboss = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])  # 가장 또렷한 필터
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.filter2D(temp, cv2.CV_8U, kernel_emboss)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def gabor(imgs, params):
    ksize = params['ksize']
    sigma = params['sigma']
    theta = params['theta']
    lambd = params['lambd']
    gamma = params['gamma']
    psi = params['psi']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = temp / 255
        kernel = cv2.getGaborKernel(ksize=(ksize, ksize), sigma=sigma, theta=theta,
                                    lambd=lambd, gamma=gamma / 100, psi=psi, ktype=cv2.CV_32F)
        kernel /= math.sqrt((kernel * kernel).sum())
        temp = cv2.filter2D(temp, -1, kernel)
        temp = cv2.cvtColor(temp.astype("uint8"), cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def high_pass(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel3x3 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
        temp = cv2.filter2D(temp, cv2.CV_8U, kernel3x3)
        imgs[i] = temp

    return imgs

def laplacian(imgs, params):
    ksize = params['ksize']
    scale = params['scale']
    delta = params['delta']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.Laplacian(temp, cv2.CV_16S, ksize=ksize, scale=scale,
                              delta=delta)  # overflow를 줄이기 위해 CV_8U를 CV_16S로 정의
        temp = cv2.convertScaleAbs(temp)  # CV_8U로 변환
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def laplacian_of_gaussian(imgs, params):
    g_ksize = params['g_ksize']
    g_sigmaX = params['g_sigmaX']
    g_sigmaY = params['g_sigmaY']
    ksize = params['ksize']
    scale = params['scale']
    delta = params['delta']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.GaussianBlur(temp, ksize=(g_ksize, g_ksize), sigmaX=g_sigmaX, sigmaY=g_sigmaY)
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        temp = cv2.Laplacian(temp, cv2.CV_16S, ksize=ksize, scale=scale, delta=delta)  # overflow를 줄이기 위해 CV_8U를 CV_16S로 정의
        temp = cv2.convertScaleAbs(temp)  # CV_8U로 변환
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def prewitt(imgs, params):
    alpha = params['alpha']
    beta = params['beta']
    gamma = params['gamma']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        kernel_x = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernel_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        grad_x = cv2.filter2D(temp, cv2.CV_16S, kernel_x)
        grad_y = cv2.filter2D(temp, cv2.CV_16S, kernel_y)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        temp = cv2.addWeighted(abs_grad_x, alpha / 10, abs_grad_y, beta / 10, gamma)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def roberts(imgs, params):
    alpha = params['alpha']
    beta = params['beta']
    gamma = params['gamma']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        Kernel_X = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 0]])
        Kernel_Y = np.array([[0, 0, -1], [0, 1, 0], [0, 0, 0]])
        grad_x = cv2.filter2D(temp, cv2.CV_16S, Kernel_X)
        grad_y = cv2.filter2D(temp, cv2.CV_16S, Kernel_Y)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        temp = cv2.addWeighted(abs_grad_x, alpha / 10, abs_grad_y, beta / 10, gamma)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def scharr(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        scharrx = cv2.Scharr(temp, ddepth=-1, dx=1, dy=0)  # 세로 경계선 감지
        scharry = cv2.Scharr(temp, ddepth=-1, dx=0, dy=1)  # 가로 경계선 감지
        temp = scharrx + scharry
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def sobel(imgs, params):
    ksize = params['ksize']
    scale = params['scale']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        SobelX = cv2.Sobel(temp, cv2.CV_8U, 0, 1, ksize=ksize, scale=scale / 10)
        SobelY = cv2.Sobel(temp, cv2.CV_8U, 1, 0, ksize=ksize, scale=scale / 10)
        temp = abs(SobelX) + abs(SobelY)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(temp)
        temp = cv2.convertScaleAbs(temp, alpha=-255 / max_val, beta=0)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

############################################ Morphology
def blackhat(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.morphologyEx(temp, cv2.MORPH_BLACKHAT, kernel, iterations=iterations)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def closing(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.morphologyEx(temp, cv2.MORPH_CLOSE, kernel, iterations=iterations)
        imgs[i] = temp

    return imgs

def dilation(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.dilate(temp, kernel, iterations=iterations)
        imgs[i] = temp

    return imgs

def erosion(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.erode(temp, kernel, iterations=iterations)
        imgs[i] = temp

    return imgs

def gradient(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.morphologyEx(temp, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def opening(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.morphologyEx(temp, cv2.MORPH_OPEN, kernel, iterations=iterations)
        imgs[i] = temp

    return imgs

def tophat(imgs, params):
    ksize = params['ksize']
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((ksize, ksize), np.uint8)
        temp = cv2.morphologyEx(temp, cv2.MORPH_TOPHAT, kernel, iterations=iterations)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

############################################ Smoothing
def averaging(imgs, params):
    ksize = params['ksize']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.blur(temp, ksize=(ksize, ksize))
        imgs[i] = temp

    return imgs

def bilateral(imgs, params):
    d = params['d']
    sigma_color = params['sigma_color']
    sigma_space = params['sigma_space']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.bilateralFilter(temp, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)
        imgs[i] = temp

    return imgs

def gaussian(imgs, params):
    ksize = params['ksize']
    sigmaX = params['sigmaX']
    sigmaY = params['sigmaY']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.GaussianBlur(temp, ksize=(ksize, ksize), sigmaX=sigmaX, sigmaY=sigmaY)
        imgs[i] = temp

    return imgs

def median(imgs, params):
    ksize = params['ksize']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.medianBlur(temp, ksize=ksize)
        imgs[i] = temp

    return imgs

def motion_smoothing(imgs, params):
    ksize = params['ksize']

    for i in range(len(imgs)):
        temp = imgs[i]
        motion_blur = np.zeros((ksize, ksize))
        motion_blur[int((ksize - 1) / 2), :] = np.ones(ksize)  # horizontal
        # motion_blur[:, int((ksize - 1) / 2)] = np.ones(ksize) # vertical
        motion_blur = motion_blur / ksize
        temp = cv2.filter2D(temp, -1, motion_blur)
        imgs[i] = temp

    return imgs

def radial_smoothing(imgs, params):
    iterations = params['iterations']

    for i in range(len(imgs)):
        temp = imgs[i]
        w, h = temp.shape[:2]
        center_x = w / 2
        center_y = h / 2
        blur = 0.01  # blur radius per pixels from center. 2px blur at 100px from center
        growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x) * blur), (w, 1)).astype(np.float32)
        shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x) * blur), (w, 1)).astype(np.float32)
        growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y) * blur), (h, 1)).transpose().astype(np.float32)
        shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y) * blur), (h, 1)).transpose().astype(np.float32)

        for j in range(iterations):
            tmp1 = cv2.remap(temp, growMapx, growMapy, cv2.INTER_LINEAR)
            tmp2 = cv2.remap(temp, shrinkMapx, shrinkMapy, cv2.INTER_LINEAR)
            temp = cv2.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)

        imgs[i] = temp

    return imgs

def watercolor(imgs, params):

    d = params['d']
    sigma_color = params['sigma_color']
    sigma_space = params['sigma_space']
    iterate = params['iterate']

    for i in range(len(imgs)):
        temp = imgs[i]

        for j in range(0, iterate):
            temp = cv2.bilateralFilter(temp, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)

        imgs[i] = temp

    return imgs

############################################ Sharpening
def sharpen(imgs, params):
    alpha = params['alpha']

    for i in range(len(imgs)):
        temp = imgs[i]
        kernel_sharpen = np.array([[0, -alpha, 0], [-alpha, 1 + 4 * alpha, -alpha], [0, -alpha, 0]])
        temp = cv2.filter2D(temp, cv2.CV_8U, kernel_sharpen)
        imgs[i] = temp

    return imgs

def unsharp(imgs, params):
    gksize = params['gksize']
    sigmaX = params['sigmaX']
    sigmaY = params['sigmaY']
    weight = params['weight']
    gamma = params['gamma']

    for i in range(len(imgs)):
        temp = imgs[i]
        gaussian_img = cv2.GaussianBlur(temp, ksize=(gksize, gksize), sigmaX=sigmaX / 100, sigmaY=sigmaY / 100)
        temp = cv2.addWeighted(src1=temp, alpha=1.0 + weight, src2=gaussian_img, beta=(-1) * weight, gamma=gamma)
        imgs[i] = temp

    return imgs

def SSR(imgs, params):
    ksize = params['ksize']

    for i in range(len(imgs)):
        temp = imgs[i]
        b, g, r = cv2.split(temp)
        b_ssr = before_SSR(b, ksize)
        g_ssr = before_SSR(g, ksize)
        r_ssr = before_SSR(r, ksize)
        temp = cv2.merge([b_ssr, g_ssr, r_ssr])
        imgs[i] = temp

    return imgs

def MSR(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        scales = [15, 101, 301]  # [3, 5, 9] # 별 차이 없음
        b, g, r = cv2.split(temp)
        b_ssr = before_MSR(b, scales)
        g_ssr = before_MSR(g, scales)
        r_ssr = before_MSR(r, scales)
        temp = cv2.merge([b_ssr, g_ssr, r_ssr])
        imgs[i] = temp

    return imgs

def MSRCR(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = np.float64(temp) + 1.0
        img_retinex = multiScaleRetinex(temp, [15, 101, 301])
        img_color = colorRestoration(temp, 125.0, 46.0)
        img_msrcr = 5.0 * (img_retinex * img_color + 25.0)

        for j in range(img_msrcr.shape[2]):
            img_msrcr[:, :, j] = (img_msrcr[:, :, j] - np.min(img_msrcr[:, :, j])) / \
                                 (np.max(img_msrcr[:, :, j]) - np.min(img_msrcr[:, :, j])) * \
                                 255

        img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))
        temp = simplestColorBalance(img_msrcr, 0.01, 0.99)

        imgs[i] = temp

    return imgs

def MSRCP(imgs, params):
    for i in range(len(imgs)):
        temp = imgs[i]

        img = np.float64(temp) + 1.0
        intensity = np.sum(img, axis=2) / img.shape[2]
        retinex = multiScaleRetinex(intensity, [15, 101, 301])
        intensity = np.expand_dims(intensity, 2)
        retinex = np.expand_dims(retinex, 2)
        intensity1 = simplestColorBalance(retinex, 0.01, 0.99)
        intensity1 = (intensity1 - np.min(intensity1)) / \
                     (np.max(intensity1) - np.min(intensity1)) * \
                     255.0 + 1.0
        img_msrcp = np.zeros_like(img)

        for y in range(img_msrcp.shape[0]):
            for x in range(img_msrcp.shape[1]):
                B = np.max(img[y, x])
                A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
                img_msrcp[y, x, 0] = A * img[y, x, 0]
                img_msrcp[y, x, 1] = A * img[y, x, 1]
                img_msrcp[y, x, 2] = A * img[y, x, 2]

        temp = np.uint8(img_msrcp - 1.0)

        imgs[i] = temp

    return imgs

############################################ Contrast
def clahe(imgs, params):
    alpha = params['alpha']
    ksize = params['ksize']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2Lab)
        l, a, b = cv2.split(temp)
        clahe = cv2.createCLAHE(clipLimit=alpha / 100, tileGridSize=(ksize, ksize))
        dst = clahe.apply(l)
        l = dst.copy()
        temp = cv2.merge((l, a, b))
        temp = cv2.cvtColor(temp, cv2.COLOR_Lab2RGB)
        imgs[i] = temp

    return imgs

def gamma_correction(imgs, params):
    gamma = params['gamma']

    for i in range(len(imgs)):
        temp = imgs[i]
        lookUpTable = np.empty((1, 256), np.uint8)
        for j in range(256):
            lookUpTable[0, j] = np.clip(pow(j / 255.0, 1.0 / (gamma / 10)) * 255.0, 0, 255)
        temp = cv2.LUT(temp, lookUpTable)
        imgs[i] = temp

    return imgs

def histogram_equalization(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        cv2.equalizeHist(temp, temp)
        image = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def histogram_equalization_color(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2Lab)
        L, a, b = cv2.split(temp)
        Hist_L = cv2.equalizeHist(L)
        L = Hist_L.copy()
        temp = cv2.merge((L, a, b))
        temp = cv2.cvtColor(temp, cv2.COLOR_Lab2RGB)
        imgs[i] = temp

    return imgs

def logarithmic_transform(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        c = 255 / np.log(1 + np.max(temp))
        temp = c * (np.log(temp + 1e-5))
        temp = np.array(temp, dtype=np.uint8)
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def saturation_intensity_correction(imgs, params):
    alpha = params['alpha']

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_RGB2HSV).astype("float32")  # 깨짐 방지
        h, s, v = cv2.split(temp)
        s = s * alpha
        s = np.clip(s, 0, 255)
        temp = cv2.merge([h, s, v])
        temp = cv2.cvtColor(temp.astype("uint8"), cv2.COLOR_HSV2RGB)  # 깨짐 방지
        imgs[i] = temp

    return imgs

############################################ Corner Detection
def BRIEF(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        star = cv2.xfeatures2d.StarDetector_create()
        brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
        kp = star.detect(temp, None)
        kp, des = brief.compute(temp, kp)
        temp = cv2.drawKeypoints(temp, kp, None, (0, 0, 255))
        imgs[i] = temp

    return imgs

def FAST(imgs, params):
    threshold = params['threshold']

    for i in range(len(imgs)):
        temp = imgs[i]
        fast = cv2.FastFeatureDetector_create()
        fast.setThreshold(threshold)  # 인근 픽셀 화소값 비교를 위한 임계치 기본값(10)
        kp = fast.detect(temp, None)
        temp = cv2.drawKeypoints(temp, kp, None)
        imgs[i] = temp

    return imgs

def harris(imgs, params):
    blocksize = params['blocksize']
    ksize = params['ksize']
    k = params['k']

    for i in range(len(imgs)):
        temp = imgs[i]
        gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, blockSize=blocksize, ksize=ksize, k=k / 100)
        image2 = temp.copy()
        image2[dst > k * dst.max()] = [0, 0, 255]
        temp = image2.copy()
        imgs[i] = temp

    return imgs

def harris_advanced(imgs, params):
    blocksize = params['blocksize']
    ksize = params['ksize']
    k = params['k']

    for i in range(len(imgs)):
        temp = imgs[i]
        gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        # find Harris Corner
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, blockSize=blocksize, ksize=ksize, k=k / 100)
        dst = cv2.dilate(dst, None)
        ret, dst = cv2.threshold(dst, k * dst.max(), 255, 0)
        dst = np.uint8(dst)
        # find centroids
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
        # define the criteria to stop and refine the corners
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv2.cornerSubPix(gray, np.float32(centroids), winSize=(5, 5), zeroZone=(-1, -1), criteria=criteria)
        res = np.hstack((centroids, corners))
        res = np.int0(res)
        temp[res[:, 3], res[:, 2]] = [0, 0, 0]
        imgs[i] = temp

    return imgs

def LBP(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        h, w, _ = temp.shape
        img_gray = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
        img_lbp = np.zeros((h, w), np.uint8)
        for j in range(0, h):
            for k in range(0, w):
                img_lbp[j, k] = lbp_calculated_pixel(img_gray, j, k)
        temp = img_lbp.copy()
        temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
        imgs[i] = temp

    return imgs

def MSER(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        mser = cv2.MSER_create()
        regions, _ = mser.detectRegions(gray)

        image_mser = temp.copy()
        for region in regions:
            # fit a bounding box to the contour
            (x, y, w, h) = cv2.boundingRect(np.reshape(region, (-1, 1, 2)))
            cv2.rectangle(image_mser, (x, y), (x + w, y + h), (0, 0, 255), 1)
        temp = image_mser.copy()
        imgs[i] = temp

    return imgs

def ORB(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        orb = cv2.ORB_create()
        kp, des = orb.detectAndCompute(temp, None)
        temp = cv2.drawKeypoints(temp, kp, None, (0, 0, 255), flags=0)
        imgs[i] = temp

    return imgs

def shi_tomasi(imgs, params):
    maxcorners = params['maxcorners']
    qualitylevel = params['qualitylevel']
    mindistance = params['mindistance']

    for i in range(len(imgs)):
        temp = imgs[i]
        gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, maxCorners=maxcorners, qualityLevel=qualitylevel / 100,
                                          minDistance=mindistance)
        corners = np.int0(corners)
        image2 = temp.copy()
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(image2, (x, y), 3, (0, 0, 255), -1)
        temp = image2.copy()
        imgs[i] = temp

    return imgs

def SIFT(imgs, params):

    for i in range(len(imgs)):
        temp = imgs[i]
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        sift = cv2.xfeatures2d.SIFT_create()
        kp = sift.detect(temp, None)
        temp = cv2.drawKeypoints(temp, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        imgs[i] = temp

    return imgs

#############################################################################################
################## 보조적으로 사용되는 메소드들

# SSR / MSR
def replaceZeroes(data):
    min_nonzero = min(data[np.nonzero(data)])
    data[data == 0] = min_nonzero
    return data

# SSR
def before_SSR(src_img, size):
    L_blur = cv2.GaussianBlur(src_img, (size, size), 0)
    img = replaceZeroes(src_img)
    L_blur = replaceZeroes(L_blur)

    dst_Img = cv2.log(img / 255.0)
    dst_Lblur = cv2.log(L_blur / 255.0)
    dst_IxL = cv2.multiply(dst_Img, dst_Lblur)
    log_R = cv2.subtract(dst_Img, dst_IxL)

    dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)
    log_uint8 = cv2.convertScaleAbs(dst_R)
    return log_uint8

# MSR
def before_MSR(img, scales):
    weight = 1 / 3.0
    scales_size = len(scales)
    h, w = img.shape[:2]
    log_R = np.zeros((h, w), dtype=np.float32)

    for i in range(scales_size):
        img = replaceZeroes(img)
        L_blur = cv2.GaussianBlur(img, (scales[i], scales[i]), 0)
        L_blur = replaceZeroes(L_blur)
        dst_Img = cv2.log(img / 255.0)
        dst_Lblur = cv2.log(L_blur / 255.0)
        dst_Ixl = cv2.multiply(dst_Img, dst_Lblur)
        log_R += weight * cv2.subtract(dst_Img, dst_Ixl)

    dst_R = cv2.normalize(log_R, None, 0, 255, cv2.NORM_MINMAX)
    log_uint8 = cv2.convertScaleAbs(dst_R)
    return log_uint8

# MSRCR / MSRCP
def singleScaleRetinex(img, sigma):
    retinex = np.log10(img) - np.log10(cv2.GaussianBlur(img, (0, 0), sigma))

    return retinex

# MSRCR / MSRCP
def multiScaleRetinex(img, sigma_list):
    retinex = np.zeros_like(img).astype(np.float64)
    for sigma in sigma_list:
        retinex += singleScaleRetinex(img, sigma)

    retinex = retinex / len(sigma_list)

    return retinex

# MSRCR / MSRCP
def simplestColorBalance(img, low_clip, high_clip):

    total = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c

        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)

    return img

# MSRCR
def colorRestoration(img, alpha, beta):

    img_sum = np.sum(img, axis=2, keepdims=True)

    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))

    return color_restoration

# lbp
def get_pixel(img, center, x, y):
    new_value = 0
    try:
        # If local neighbourhood pixel
        # value is greater than or equal
        # to center pixel values then
        # set it to 1
        if img[x][y] >= center:
            new_value = 1
    except:
        # Exception is required when
        # neighbourhood value of a center
        # pixel value is null i.e. values
        # present at boundaries.
        pass
    return new_value

# lbp
def lbp_calculated_pixel(img, x, y):
    center = img[x][y]
    val_ar = []
    # top_left
    val_ar.append(get_pixel(img, center, x - 1, y - 1))
    # top
    val_ar.append(get_pixel(img, center, x - 1, y))
    # top_right
    val_ar.append(get_pixel(img, center, x - 1, y + 1))
    # right
    val_ar.append(get_pixel(img, center, x, y + 1))
    # bottom_right
    val_ar.append(get_pixel(img, center, x + 1, y + 1))
    # bottom
    val_ar.append(get_pixel(img, center, x + 1, y))
    # bottom_left
    val_ar.append(get_pixel(img, center, x + 1, y - 1))
    # left
    val_ar.append(get_pixel(img, center, x, y - 1))
    # Now, we need to convert binary
    # values to decimal
    power_val = [1, 2, 4, 8, 16, 32, 64, 128]
    val = 0
    for i in range(len(val_ar)):
        val += val_ar[i] * power_val[i]
    return val
