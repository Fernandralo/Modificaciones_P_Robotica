import cv2
import numpy as np
import pytesseract
import numpy as np

#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1/bin/tesseract'


def shape_recognition(rutaImagen: str):


    imagen = cv2.imread(rutaImagen)  # Reemplaza 'ruta/de/la/imagen.jpg' con la ruta de tu imagen

    alto, ancho, _ = imagen.shape

    # RECONOCIMIENTO DE FIGURA
    region_superior = imagen[0:int(alto/3),:]

    region_superior_gris = cv2.cvtColor(region_superior, cv2.COLOR_BGR2GRAY)

    _, region_superior_binaria = cv2.threshold(region_superior_gris, 127, 255, cv2.THRESH_BINARY)

    contornos, _ = cv2.findContours(region_superior_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    figuras = []

    for contorno in contornos:
        # Aproximar el contorno a una figura de pocos lados
        approx = cv2.approxPolyDP(contorno, 0.04 * cv2.arcLength(contorno, True), True)
        lados = len(approx)

        # Determinar el tipo de figura basado en el número de lados
        if lados == 3:
            tipo_figura = "Triangulo"
        elif lados == 4:
            x, y, ancho, alto = cv2.boundingRect(approx)
            aspect_ratio = float(ancho) / alto

            # Si el aspect ratio está cerca de 1, es un cuadrado; de lo contrario, es un rectángulo
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                tipo_figura = "Cuadrado"
            else:
                tipo_figura = "Rectangulo"
        elif lados == 5:
            tipo_figura = "Pentagono"
        elif lados == 6:
            tipo_figura = "Hexagono"
        else:
            # Comprobar si es un círculo
            area = cv2.contourArea(contorno)
            perimetro = cv2.arcLength(contorno, True)
            circularidad = 4 * np.pi * area / (perimetro ** 2)

            if circularidad >= 0.85:
                tipo_figura = "Circulo"
            else:
                tipo_figura = "Desconocido"

        # Agregar la figura reconocida a la lista
        figuras.append(tipo_figura)

    # Dibujar los contornos y etiquetas en la imagen completa
    imagen = cv2.drawContours(imagen, contornos, -1, (0, 255, 0), 2)

    for i, figura in enumerate(figuras):
        x, y, _, _ = cv2.boundingRect(contornos[i])
        cv2.putText(imagen, figura, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return region_superior




def text_recognition(ruta_imagen):
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    
    # Obtener la región horizontal de la imagen (1/3 de la altura)
    altura, ancho, _ = imagen.shape
    region_horizontal = imagen[altura//3:2*altura//3, :]
    
    # Convertir la región a escala de grises
    gris = cv2.cvtColor(region_horizontal, cv2.COLOR_BGR2GRAY)
    
    # Aplicar umbralización adaptativa para resaltar el texto
    _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Obtener el texto reconocido usando Tesseract OCR
    texto = pytesseract.image_to_string(umbral, lang='eng')
    
    # Encontrar los contornos de las palabras
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contorno in contornos:
        # Calcular el rectángulo del contorno
        (x, y, w, h) = cv2.boundingRect(contorno)
        
        # Dibujar el rectángulo
        cv2.rectangle(imagen, (x, y + altura//3), (x + w, y + altura//3 + h), (0, 255, 0), 2)
    
    # Posicionar el texto en el centro de la región horizontal
    pos_x = 50
    pos_y = altura//3 + 50
    cv2.putText(imagen, texto, (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Devolver la imagen resultante
    return region_horizontal

def color_recognition(rutaImagen:str):
    imagen = cv2.imread(rutaImagen)  # Ruta de la imagen que deseas cargar

    alto, ancho, _ = imagen.shape
        
    region_baja = imagen[int(2*alto/3):alto, :]
    
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
    upper_pink = np.array([180, 255, 255]) 
    
    lower_orange = np.array([10, 50, 50])  # Rango inferior del color naranja en HSV
    upper_orange = np.array([20, 255, 255]) # Rango superior del color rosa en HSV
    
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
    cv2.drawContours(region_baja, contours_orange, -1, (0, 165, 255), 2)

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
    
    # Mostrar el nombre del color sobre los contornos
    for contour in contours_blue:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Azul", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["blue"], 2)
    
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Rojo", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["red"], 2)
    
    for contour in contours_green:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Verde", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["green"], 2)
    
    for contour in contours_yellow:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Amarillo", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["yellow"], 2)
    
    for contour in contours_purple:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Morado", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["purple"], 2)
    
    for contour in contours_gray:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Gris", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["gray"], 2)
    
    for contour in contours_pink:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Rosa", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["pink"], 2)
    for contour in contours_orange:
        x,y,w,h = cv2.boundingRect(contour)
        cv2.putText(region_baja, "Naranja", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_labels["orange"], 2)

    # Mostrar la imagen original con los contornos y etiqueta

    return region_baja


def obtener_figura(rutaArchivo:str):
    region_alta = shape_recognition(rutaArchivo)
    region_media = text_recognition(rutaArchivo)
    region_baja = color_recognition(rutaArchivo)

    concatenado = cv2.vconcat([region_alta,region_media,region_baja])

    cv2.imwrite("resultado.png",concatenado)
    cv2.imread("Prueba",concatenado)


obtener_figura("imagen.png")

