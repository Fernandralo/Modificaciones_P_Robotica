import cv2 as cv
import numpy as np

#shape counter
cir=0
tri=0
quad=0
pen=0
hexa=0

#capture video through picam 
cap = cv.VideoCapture(1)
cap.set(3, 320)  # set video width
cap.set(4, 250)  # set video height

while True:
    ret, img = cap.read()
    img = cv.flip(img,-1)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    
    ret, thresh = cv.threshold(blur, 60, 255, cv.CHAIN_APPROX_NONE)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    i=0
    for cnt in contours:
        #have to skip the first contour as usually it is the frame itself
        if i==0:
            i=1
            continue

        if cv.contourArea(cnt)>110:
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), True)

            #draw the shapes outline using drawContour()
            cv.drawContours(img, [cnt], 0, (0, 255, 0),1)

            #finding center point of the detected shape
            c = cv.moments(cnt)
            if c['m00'] != 0:
                x = int(c['m10'] / c['m00'])
                y = int(c['m01'] / c['m00'])

                #putting name from the center of the shape
                if len(approx) == 3:
                    cv.putText(img, 'Triangulo', (x, y),
                                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    tri+=1


                elif len(approx) == 4:
                    cv.putText(img, 'Cuadrilatero', (x, y),
                                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    quad+=1


                elif len(approx) == 5:
                    cv.putText(img, 'Pentagono', (x, y),
                                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    pen+=1

                elif len(approx) == 6:
                    cv.putText(img, 'Hexagono', (x, y),
                                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    hexa+=1

                else:
                    cv.putText(img, 'CCirculo', (x, y),
                                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    cir+=1
                

    cv.imshow('live0',img)
    cv.imshow('live1', thresh)
    #cv.imshow('live2', dilation)
    
    #print out the shape counter
    print('*******************\nCircle:',cir)
    print('Triangulo:',int(tri/2))
    print('Cuadrilatero:',int(quad/2))
    print('Pentagono:',int(pen/2))
    print('Hexagono:',int(hexa/2))
    print('Total formas:',int((cir+tri+quad+pen+hexa)/2))
    
    #reset counter at each frame
    cir=0
    tri=0
    quad=0
    pen=0
    hexa=0
    
    k = cv.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap.release()
cv.destroyAllWindows()