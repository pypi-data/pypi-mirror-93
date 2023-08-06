import math

import cv2
import numpy as np


# 전처리될 필터 모음
############################################ Binarization
# Threshold binary
def threshold_binary(img, params):
    thresh = params['thresh']
    maxvalue = params['maxvalue']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=thresh, maxval=maxvalue, type=cv2.THRESH_BINARY)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# Threshold binary inverse
def threshold_binary_inverse(img, params):
    thresh = params['thresh']
    maxvalue = params['maxvalue']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=thresh, maxval=maxvalue, type=cv2.THRESH_BINARY_INV)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# Threshold truncate
def threshold_truncate(img, params):
    thresh = params['thresh']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=thresh, maxval=0, type=cv2.THRESH_TRUNC)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# Threshold tozero
def threshold_tozero(img, params):
    thresh = params['thresh']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=thresh, maxval=0, type=cv2.THRESH_TOZERO)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# threshold_tozero_inverse
def threshold_tozero_inverse(img, params):
    thresh = params['thresh']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=thresh, maxval=0, type=cv2.THRESH_TOZERO_INV)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# threshold_triangle
def threshold_triangle(img, params):
    maxvalue = params['maxvalue']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=0, maxval=maxvalue, type=cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# threshold_otsu
def threshold_otsu(img, params):
    maxvalue = params['maxvalue']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, temp = cv2.threshold(temp, thresh=0, maxval=maxvalue, type=cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# adaptive_threshold_gaussian_c
def adaptive_threshold_gaussian_c(img, params):
    maxvalue = params['maxvalue']
    block_size = params['block_size']
    c = params['c']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = cv2.adaptiveThreshold(temp, maxValue=maxvalue, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 thresholdType=cv2.THRESH_BINARY, blockSize=block_size, C=c)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# adaptive_threshold_mean_c
def adaptive_threshold_mean_c(img, params):
    maxvalue = params['maxvalue']
    block_size = params['block_size']
    c = params['c']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = cv2.adaptiveThreshold(temp, maxValue=maxvalue, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                 thresholdType=cv2.THRESH_BINARY, blockSize=block_size, C=c)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

############################################ Colormodel
# grayscale
def grayscale(img, params):
    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# hsv
def hsv(img, params):
    temp = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    return temp

############################################ Edge
# basic_gradient_kernel
def basic_gradient_kernel(img, params):
    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gx_kernel = np.array([[-1, 1]])
    gy_kernel = np.array([[-1], [1]])
    edge_gx = cv2.filter2D(temp, -1, gx_kernel)
    edge_gy = cv2.filter2D(temp, -1, gy_kernel)
    basic = edge_gx + edge_gy
    temp = cv2.cvtColor(basic, cv2.COLOR_GRAY2RGB)
    return temp

# canny
def canny(img, params):
    threshold1 = params['threshold1']
    threshold2 = params['threshold2']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(temp, threshold1=threshold1, threshold2=threshold2)
    temp = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
    return temp

# difference_of_gaussian
def difference_of_gaussian(img, params):
    ksize_1 = params['ksize_1']
    sigmaX_1 = params['sigmaX_1']
    sigmaY_1 = params['sigmaY_1']
    ksize_2 = params['ksize_2']
    sigmaX_2 = params['sigmaX_2']
    sigmaY_2 = params['sigmaY_2']

    low = cv2.GaussianBlur(img, ksize=(ksize_1, ksize_1), sigmaX=sigmaX_1, sigmaY=sigmaY_1)
    high = cv2.GaussianBlur(img, ksize=(ksize_2, ksize_2), sigmaX=sigmaX_2, sigmaY=sigmaY_2)
    low_gray = cv2.cvtColor(low, cv2.COLOR_RGB2GRAY)
    high_gray = cv2.cvtColor(high, cv2.COLOR_RGB2GRAY)
    dog = low_gray - high_gray
    temp = cv2.cvtColor(dog, cv2.COLOR_GRAY2RGB)
    return temp

# emboss
def emboss(img, params):
    kernel_emboss = np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])  # 가장 또렷한 필터
    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = cv2.filter2D(temp, cv2.CV_8U, kernel_emboss)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# gabor
def gabor(img, params):
    ksize = params['ksize']
    sigma = params['sigma']
    theta = params['theta']
    lambd = params['lambd']
    gamma = params['gamma']
    psi = params['psi']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = temp / 255
    kernel = cv2.getGaborKernel(ksize=(ksize, ksize), sigma=sigma, theta=theta,
                                lambd=lambd, gamma=gamma / 100, psi=psi, ktype=cv2.CV_32F)
    kernel /= math.sqrt((kernel * kernel).sum())
    temp = cv2.filter2D(temp, -1, kernel)
    temp = cv2.cvtColor(temp.astype("uint8"), cv2.COLOR_GRAY2RGB)
    return temp

# high_pass
def high_pass(img, params):
    kernel3x3 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    temp = cv2.filter2D(img, cv2.CV_8U, kernel3x3)
    return temp

# laplacian
def laplacian(img, params):
    ksize = params['ksize']
    scale = params['scale']
    delta = params['delta']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    temp = cv2.Laplacian(temp, cv2.CV_16S, ksize=ksize, scale=scale,
                         delta=delta)  # overflow를 줄이기 위해 CV_8U를 CV_16S로 정의
    laplacian = cv2.convertScaleAbs(temp)  # CV_8U로 변환
    temp = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2RGB)
    return temp

# laplacian_of_gaussian
def laplacian_of_gaussian(img, params):
    g_ksize = params['g_ksize']
    g_sigmaX = params['g_sigmaX']
    g_sigmaY = params['g_sigmaY']
    ksize = params['ksize']
    scale = params['scale']
    delta = params['delta']

    temp = cv2.GaussianBlur(img, ksize=(g_ksize, g_ksize), sigmaX=g_sigmaX, sigmaY=g_sigmaY)
    temp = cv2.cvtColor(temp, cv2.COLOR_RGB2GRAY)
    temp = cv2.Laplacian(temp, cv2.CV_16S, ksize=ksize, scale=scale, delta=delta)
    laplacian_gaussian = cv2.convertScaleAbs(temp)  # CV_8U로 변환
    temp = cv2.cvtColor(laplacian_gaussian, cv2.COLOR_GRAY2RGB)
    return temp

# prewitt
def prewitt(img, params):
    alpha = params['alpha']
    beta = params['beta']
    gamma = params['gamma']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel_x = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernel_y = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    grad_x = cv2.filter2D(temp, cv2.CV_16S, kernel_x)
    grad_y = cv2.filter2D(temp, cv2.CV_16S, kernel_y)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    temp = cv2.addWeighted(abs_grad_x, alpha / 10, abs_grad_y, beta / 10, gamma)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# roberts
def roberts(img, params):
    alpha = params['alpha']
    beta = params['beta']
    gamma = params['gamma']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    Kernel_X = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 0]])
    Kernel_Y = np.array([[0, 0, -1], [0, 1, 0], [0, 0, 0]])

    grad_x = cv2.filter2D(temp, cv2.CV_16S, Kernel_X)
    grad_y = cv2.filter2D(temp, cv2.CV_16S, Kernel_Y)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    temp = cv2.addWeighted(abs_grad_x, alpha / 10, abs_grad_y, beta / 10, gamma)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# scharr
def scharr(img, params):
    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    scharrx = cv2.Scharr(temp, ddepth=-1, dx=1, dy=0)  # 세로 경계선 감지
    scharry = cv2.Scharr(temp, ddepth=-1, dx=0, dy=1)  # 가로 경계선 감지
    temp = scharrx + scharry
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# sobel
def sobel(img, params):
    ksize = params['ksize']
    scale = params['scale']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    SobelX = cv2.Sobel(temp, cv2.CV_8U, 0, 1, ksize=ksize, scale=scale / 10)
    SobelY = cv2.Sobel(temp, cv2.CV_8U, 1, 0, ksize=ksize, scale=scale / 10)
    sobel = abs(SobelX) + abs(SobelY)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(sobel)
    SobelImage = cv2.convertScaleAbs(sobel, alpha=-255 / max_val, beta=0)
    temp = cv2.cvtColor(SobelImage, cv2.COLOR_GRAY2RGB)
    return temp

############################################ Morphology
# blackhat
def blackhat(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.morphologyEx(temp, cv2.MORPH_BLACKHAT, kernel, iterations=iterations)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# closing
def closing(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    return temp

# dilation
def dilation(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.dilate(img, kernel, iterations=iterations)
    return temp

# erosion
def erosion(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.erode(img, kernel, iterations=iterations)
    return temp

# gradient
def gradient(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.morphologyEx(temp, cv2.MORPH_GRADIENT, kernel, iterations=iterations)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

# opening
def opening(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
    return temp

# tophat
def tophat(img, params):
    ksize = params['ksize']
    iterations = params['iterations']

    temp = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((ksize, ksize), np.uint8)
    temp = cv2.morphologyEx(temp, cv2.MORPH_TOPHAT, kernel, iterations=iterations)
    temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2RGB)
    return temp

############################################ Smoothing
# averaging
def averaging(img, params):
    ksize = params['ksize']

    temp = cv2.blur(img, ksize=(ksize, ksize))
    return temp

# bilateral
def bilateral(img, params):
    d = params['d']
    sigma_color = params['sigma_color']
    sigma_space = params['sigma_space']

    temp = cv2.bilateralFilter(img, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)
    return temp

# gaussian
def gaussian(img, params):
    ksize = params['ksize']
    sigmaX = params['sigmaX']
    sigmaY = params['sigmaY']

    temp = cv2.GaussianBlur(img, ksize=(ksize, ksize), sigmaX=sigmaX, sigmaY=sigmaY)
    return temp

# median
def median(img, params):
    ksize = params['ksize']

    temp = cv2.medianBlur(img, ksize=ksize)
    return temp

# motion_smoothing
def motion_smoothing(img, params):
    ksize = params['ksize']

    motion_blur = np.zeros((ksize, ksize))
    motion_blur[int((ksize - 1) / 2), :] = np.ones(ksize)  # horizontal
    # motion_blur[:, int((ksize - 1) / 2)] = np.ones(ksize) # vertical
    motion_blur = motion_blur / ksize
    temp = cv2.filter2D(img, -1, motion_blur)
    return temp

# radial_smoothing
def radial_smoothing(img, params):
    iterations = params['iterations']

    temp = img
    w, h = temp.shape[:2]
    center_x = w / 2
    center_y = h / 2
    blur = 0.01  # blur radius per pixels from center. 2px blur at 100px from center
    growMapx = np.tile(np.arange(h) + ((np.arange(h) - center_x) * blur), (w, 1)).astype(np.float32)
    shrinkMapx = np.tile(np.arange(h) - ((np.arange(h) - center_x) * blur), (w, 1)).astype(np.float32)
    growMapy = np.tile(np.arange(w) + ((np.arange(w) - center_y) * blur), (h, 1)).transpose().astype(np.float32)
    shrinkMapy = np.tile(np.arange(w) - ((np.arange(w) - center_y) * blur), (h, 1)).transpose().astype(np.float32)
    for i in range(iterations):
        tmp1 = cv2.remap(temp, growMapx, growMapy, cv2.INTER_LINEAR)
        tmp2 = cv2.remap(temp, shrinkMapx, shrinkMapy, cv2.INTER_LINEAR)
        temp = cv2.addWeighted(tmp1, 0.5, tmp2, 0.5, 0)
    return temp

# watercolor
def watercolor(img, params):
    d = params['d']
    sigma_color = params['sigma_color']
    sigma_space = params['sigma_space']
    iterate = params['iterate']

    temp = img
    for i in range(0, iterate):
        temp = cv2.bilateralFilter(temp, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)

    return temp

############################################ Sharpening
# sharpen
def sharpen(img, params):
    alpha = params['alpha']

    kernel_sharpen = np.array([[0, -alpha, 0], [-alpha, 1 + 4 * alpha, -alpha], [0, -alpha, 0]])
    temp = cv2.filter2D(img, cv2.CV_8U, kernel_sharpen)
    return temp

# unsharp
def unsharp(img, params):
    gksize = params['gksize']
    sigmaX = params['sigmaX']
    sigmaY = params['sigmaY']
    weight = params['weight']
    gamma = params['gamma']

    gaussian_img = cv2.GaussianBlur(img, ksize=(gksize, gksize), sigmaX=sigmaX / 100, sigmaY=sigmaY / 100)
    temp = cv2.addWeighted(src1=img, alpha=1.0 + weight, src2=gaussian_img, beta=(-1) * weight, gamma=gamma)
    return temp

# SSR
def SSR(img, params):
    ksize = params['ksize']

    b, g, r = cv2.split(img)
    b_ssr = before_SSR(b, ksize)
    g_ssr = before_SSR(g, ksize)
    r_ssr = before_SSR(r, ksize)
    temp = cv2.merge([b_ssr, g_ssr, r_ssr])
    return temp

# MSR
def MSR(img, params):
    scales = [15, 101, 301]  # [3, 5, 9] # 별 차이 없음
    b, g, r = cv2.split(img)
    b_msr = before_MSR(b, scales)
    g_msr = before_MSR(g, scales)
    r_msr = before_MSR(r, scales)
    temp = cv2.merge([b_msr, g_msr, r_msr])
    return temp

# MSRCR
def MSRCR(img, params):
    image = np.float64(img) + 1.0
    img_retinex = multiScaleRetinex(image, [15, 101, 301])
    img_color = colorRestoration(image, 125.0, 46.0)
    img_msrcr = 5.0 * (img_retinex * img_color + 25.0)

    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255

    img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))
    temp = simplestColorBalance(img_msrcr, 0.01, 0.99)
    return temp

# MSRCP
def MSRCP(img, params):
    image = np.float64(img) + 1.0
    intensity = np.sum(image, axis=2) / image.shape[2]
    retinex = multiScaleRetinex(intensity, [15, 101, 301])
    intensity = np.expand_dims(intensity, 2)
    retinex = np.expand_dims(retinex, 2)
    intensity1 = simplestColorBalance(retinex, 0.01, 0.99)
    intensity1 = (intensity1 - np.min(intensity1)) / \
                 (np.max(intensity1) - np.min(intensity1)) * \
                 255.0 + 1.0
    img_msrcp = np.zeros_like(image)

    for y in range(img_msrcp.shape[0]):
        for x in range(img_msrcp.shape[1]):
            B = np.max(image[y, x])
            A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
            img_msrcp[y, x, 0] = A * image[y, x, 0]
            img_msrcp[y, x, 1] = A * image[y, x, 1]
            img_msrcp[y, x, 2] = A * image[y, x, 2]

    temp = np.uint8(img_msrcp - 1.0)
    return temp

############################################ Contrast
# clahe
def clahe(img, params):
    alpha = params['alpha']
    ksize = params['ksize']

    image = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
    l, a, b = cv2.split(image)
    clahe = cv2.createCLAHE(clipLimit=alpha / 100, tileGridSize=(ksize, ksize))
    dst = clahe.apply(l)
    l = dst.copy()
    image = cv2.merge((l, a, b))
    temp = cv2.cvtColor(image, cv2.COLOR_LAB2RGB)
    return temp

# gamma_correction
def gamma_correction(img, params):
    gamma = params['gamma']

    lookUpTable = np.empty((1, 256), np.uint8)
    for j in range(256):
        lookUpTable[0, j] = np.clip(pow(j / 255.0, 1.0 / (gamma / 10)) * 255.0, 0, 255)
    temp = cv2.LUT(img, lookUpTable)
    return temp

# histogram_equalization
def histogram_equalization(img, params):

    image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.equalizeHist(image, image)
    temp = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return temp

# histogram_equalization_color
def histogram_equalization_color(img, params):
    image = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
    L, a, b = cv2.split(image)
    Hist_L = cv2.equalizeHist(L)
    L = Hist_L.copy()
    image = cv2.merge((L, a, b))
    temp = cv2.cvtColor(image, cv2.COLOR_Lab2RGB)
    return temp

# logarithmic_transform
def logarithmic_transform(img, params):
    image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    c = 255 / np.log(1 + np.max(image))
    # 1e-5를 더해주면 "RuntimeWarning: divide by zero encountered in log"오류가 나오지 않음
    image = c * (np.log(image + 1e-5))
    # Grayscale을 안해도 결과는 나오지만, 어두운 부분이 깨지는 현상이 있음
    # 색이 있는 상태로 1e-5를 더하지 않으면 결과가 올바르게 나옴 / 하지만 "RuntimeWarning: divide by zero encountered in log"오류 발생
    image = np.array(image, dtype=np.uint8)
    temp = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return temp

# saturation_intensity_correction
def saturation_intensity_correction(img, params):
    alpha = params['alpha']

    image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV).astype("float32")  # 깨짐 방지
    h, s, v = cv2.split(image)
    s = s * alpha
    s = np.clip(s, 0, 255)
    image = cv2.merge([h, s, v])
    temp = cv2.cvtColor(image.astype("uint8"), cv2.COLOR_HSV2RGB)  # 깨짐 방지
    return temp

############################################ Corner Detection
# BRIEF
def BRIEF(img, params):
    star = cv2.xfeatures2d.StarDetector_create()
    brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
    kp = star.detect(img, None)
    kp, des = brief.compute(img, kp)
    temp = cv2.drawKeypoints(img, kp, None, (0, 0, 255))
    return temp

# FAST
def FAST(img, params):
    threshold = params['threshold']

    fast = cv2.FastFeatureDetector_create()
    fast.setThreshold(threshold)  # 인근 픽셀 화소값 비교를 위한 임계치 기본값(10)
    # fast.setNonmaxSuppression(False)  # 비슷한 지점에서 너무 많은 특징점이 추출되는 것을 방지
    kp = fast.detect(img, None)
    temp = cv2.drawKeypoints(img, kp, None)
    return temp

# harris
def harris(img, params):
    blocksize = params['blocksize']
    ksize = params['ksize']
    k = params['k']

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, blockSize=blocksize, ksize=ksize, k=k / 100)
    image2 = img.copy()
    image2[dst > k * dst.max()] = [0, 0, 255]
    temp = image2.copy()
    return temp

# harris_advanced
def harris_advanced(img, params):
    blocksize = params['blocksize']
    ksize = params['ksize']
    k = params['k']

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    image2 = img.copy()
    image2[res[:, 3], res[:, 2]] = [0, 0, 255]
    temp = image2.copy()
    return temp

# LBP
def LBP(img, params):
    h, w, _ = img.shape
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_lbp = np.zeros((h, w), np.uint8)
    for i in range(0, h):
        for j in range(0, w):
            img_lbp[i, j] = lbp_calculated_pixel(img_gray, i, j)
    image = img_lbp.copy()
    temp = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    return temp

# MSER
def MSER(img, params):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mser = cv2.MSER_create()
    regions, _ = mser.detectRegions(gray)

    image_mser = img.copy()
    for region in regions:
        # fit a bounding box to the contour
        (x, y, w, h) = cv2.boundingRect(np.reshape(region, (-1, 1, 2)))
        cv2.rectangle(image_mser, (x, y), (x + w, y + h), (0, 0, 255), 1)
    temp = image_mser.copy()
    return temp

# ORB
def ORB(img, params):
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    temp = cv2.drawKeypoints(img, kp, None, (0, 0, 255), flags=0)
    return temp

# shi_tomasi
def shi_tomasi(img, params):
    maxcorners = params['maxcorners']
    qualitylevel = params['qualitylevel']
    mindistance = params['mindistance']

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=maxcorners, qualityLevel=qualitylevel / 100,
                                      minDistance=mindistance)
    corners = np.int0(corners)
    image2 = img.copy()
    for i in corners:
        x, y = i.ravel()
        cv2.circle(image2, (x, y), 3, (0, 0, 255), -1)
    temp = image2.copy()
    return temp

# SIFT
def SIFT(img, params):
    image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(image, None)
    temp = cv2.drawKeypoints(image, kp, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    return temp

#############################################################################################
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
