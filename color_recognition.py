import cv2
import numpy as np

def color_recognition(rutaImagen: str):


    imagen = cv2.imread(rutaImagen)  # Ruta de la imagen que deseas cargar

    alto, ancho, _ = imagen.shape

    region_baja = imagen[int(2 * alto / 3):alto, :]

    hsv = cv2.cvtColor(region_baja, cv2.COLOR_BGR2HSV)

    # Definir los rangos de colores que deseas reconocer
    lower_blue = np.array([100, 50, 50])  # Rango inferior del color azul en HSV
    upper_blue = np.array([130, 255, 255])  # Rango superior del color azul en HSV

    lower_red = np.array([0, 50, 50])  # Rango inferior del color rojo en HSV
    upper_red = np.array([10, 255, 255])  # Rango superior del color rojo en HSV

    lower_green = np.array([36, 50, 50])  # Rango inferior del color verde en HSV
    upper_green = np.array([70, 255, 255])  # Rango superior del color verde en HSV

    lower_yellow = np.array([20, 50, 50])  # Rango inferior del color amarillo en HSV
    upper_yellow = np.array([35, 255, 255])  # Rango superior del color amarillo en HSV

    lower_purple = np.array([130, 50, 50])  # Rango inferior del color morado en HSV
    upper_purple = np.array([160, 255, 255])  # Rango superior del color morado en HSV

    lower_gray = np.array([0, 0, 50])  # Rango inferior del color gris en HSV
    upper_gray = np.array([180, 50, 200])  # Rango superior del color gris en HSV

    lower_pink = np.array([160, 50, 50])  # Rango inferior del color rosa en HSV
    upper_pink = np.array([180, 255, 255])  # Rango superior del color rosa en HSV

    lower_orange = np.array([10, 50, 50])  # Rango inferior del color naranja en HSV
    upper_orange = np.array([20, 255, 255])  # Rango superior del color naranja en HSV

    # Aplicar máscaras para obtener solo los píxeles en los rangos de colores
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
    mask_pink = cv2.inRange(hsv, lower_pink, upper_pink)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    # Aplicar operaciones de filtrado para reducir el ruido
    kernel = np.ones((5, 5), np.uint8)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
    mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel)
    mask_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_OPEN, kernel)
    mask_gray = cv2.morphologyEx(mask_gray, cv2.MORPH_OPEN, kernel)
    mask_pink = cv2.morphologyEx(mask_pink, cv2.MORPH_OPEN, kernel)
    mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, kernel)

    # Encontrar los contornos de los objetos detectados para cada color
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_purple, _ = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_gray, _ = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_pink, _ = cv2.findContours(mask_pink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contornos en la imagen original para cada color y agregar texto
    cv2.drawContours(region_baja, contours_blue, -1, (255, 0, 0), 2)
    cv2.drawContours(region_baja, contours_red, -1, (0, 0, 255), 2)
    cv2.drawContours(region_baja, contours_green, -1, (0, 255, 0), 2)
    cv2.drawContours(region_baja, contours_yellow, -1, (0, 255, 255), 2)
    cv2.drawContours(region_baja, contours_purple, -1, (128, 0, 128), 2)
    cv2.drawContours(region_baja, contours_gray, -1, (128, 128, 128), 2)
    cv2.drawContours(region_baja, contours_pink, -1, (255, 192, 203), 2)
    cv2.drawContours(region_baja, contours_orange, -1, (0, 165, 255), 2)  # Naranja: BGR (0, 165, 255)

    # Etiquetas de los colores
    color_labels = {
        "blue": (255, 0, 0),
        "red": (0, 0, 255),
        "green": (0, 255, 0),
        "yellow": (0, 255, 255),
        "purple": (128, 0, 128),
        "gray": (128, 128, 128),
        "pink": (255, 192, 203),
        "orange": (0, 165, 255)
    }

    # Agregar texto para cada color
    for cnt in contours_blue:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Blue", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["blue"], 2)
    for cnt in contours_red:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["red"], 2)
    for cnt in contours_green:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Green", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["green"], 2)
    for cnt in contours_yellow:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Yellow", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["yellow"], 2)
    for cnt in contours_purple:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Purple", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["purple"], 2)
    for cnt in contours_gray:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Gray", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["gray"], 2)
    for cnt in contours_pink:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Pink", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["pink"], 2)
    for cnt in contours_orange:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.putText(region_baja, "Orange", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_labels["orange"], 2)

    return region_baja


region_baja = color_recognition()
cv2.imwrite("resultado.png", region_baja)
cv2.imread("Color Recognition", region_baja)


    

