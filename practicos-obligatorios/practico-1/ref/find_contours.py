import numpy as np
import cv2


chessboardSize = (4, 3)
threshold = 100

# Supongo que la esquina superior izquierda está en la primer esquina del patrón
paperSize_h = 253.3 #mm 
paperSize_v = 190 #mm

mmpx = 0.3958

#253.3mm-------------- 640px
#52mm   -------------- 131.38px

#190mm ---------------- 480px
#35mm  ---------------- 88.42px

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)



def getContours(frame):
    global threshold

    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Escala de grises
    imblur = cv2.blur(imgray, (10,10)) # Filtro blur para disminuir ruido
    ret, imthresh = cv2.threshold(imblur, threshold, 255, cv2.THRESH_BINARY) # Threshold para pasar la imagen a B/N
    
    # Parche
    cv2.rectangle(imthresh, (400, 0), (640, 150), (255,255,255), -1)
    # Calculo de contornos
    contornos, hierarchy = cv2.findContours(imthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(frame, contornos, -1, (0,255,0), 3)

    return contornos, frame



def rectify(frame):
    global n, h, v
    
    drawedFrame = frame.copy()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Escala de grises
    ret, corners = cv2.findChessboardCorners(grayFrame, chessboardSize, None, cv2.CALIB_CB_FAST_CHECK)
    

    if ret is True:
        refinedCorners = cv2.cornerSubPix(grayFrame, corners, (11, 11), (-1, -1), criteria)
        cv2.drawChessboardCorners(frame, (chessboardSize), refinedCorners, ret)
       
        # Calculo de proporcion (px/mm)
        #pxmm = (tuple(corners[1][0])[0] - tuple(corners[0][0])[0]) / 17
        #print(pxmm)

        imgSize = (frame.shape[1], frame.shape[0])
        
        # Puntos a mapear
        src = np.float32([corners[0], corners[3], corners[8], corners[11]])
        dst = np.float32([[508, 0], [640, 0], [508, 88], [640, 88]]) #
       
        cv2.circle(frame, tuple(src[0][0]), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(src[1][0]), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(src[2][0]), 5, (255, 0, 0), -1)
        cv2.circle(frame, tuple(src[3][0]), 5, (0, 255, 255), -1)
        
        cv2.circle(frame, tuple(dst[0]), 5, (0, 0, 255), -1)
        cv2.circle(frame, tuple(dst[1]), 5, (0, 255, 0), -1)
        cv2.circle(frame, tuple(dst[2]), 5, (255, 0, 0), -1)
        cv2.circle(frame, tuple(dst[3]), 5, (0, 255, 255), -1)
        

        M = cv2.getPerspectiveTransform(src, dst) 
        rectifiedFrame = cv2.warpPerspective(drawedFrame, M, imgSize)

        return True, rectifiedFrame

    else: 
        return False, frame



cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1) # Flip horizontal

    valid, rectifiedFrame = rectify(frame)
    
    if(valid):
        contornos, drawedFrame = getContours(rectifiedFrame.copy())

        # Medicion
        for contorno in contornos:
            x,y,contourW,contourH = cv2.boundingRect(contorno) # Rectangulo dentro del cual esta comprendido el objeto a medir
            cv2.line(drawedFrame, (x, y+contourH), (x+contourW, y+contourH), (0,0,255), 2) # Ancho
            cv2.line(drawedFrame, (x+contourW, y), (x+contourW, y+contourH), (0,0,255), 2) # Alto
            # Paso a mm
            contourW_mm = round(mmpx * contourW, 2)
            contourH_mm = round(mmpx * contourH, 2)
            # Etiquetas
            cv2.putText(drawedFrame, str(contourW_mm)+"mm", (round(x+contourW/2), y+contourH+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            cv2.putText(drawedFrame, str(contourH_mm)+"mm", (x+contourW, round(y+contourH/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
    
    else:
        drawedFrame = frame.copy()

    cv2.namedWindow('Salida')
    cv2.imshow('Salida', drawedFrame)
    cv2.namedWindow('Captura')
    cv2.imshow('Captura', frame)
    #cv2.namedWindow('thresh')
    #cv2.imshow('thresh', imthresh)
    #cv2.namedWindow('blur')
    #cv2.imshow('blur', imblur)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('+'):
        threshold = threshold + 1
        print(threshold)
    if key == ord('-'):
        threshold = threshold - 1
        print(threshold)
    

cap.release()
cv2.destroyAllWindows()
