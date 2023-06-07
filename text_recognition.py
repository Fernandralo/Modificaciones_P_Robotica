import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.1/bin/tesseract'

def reconocer_texto_camara():
    # Capturar video de la cámara
    captura = cv2.VideoCapture(0)
    
    while True:
        # Leer fotograma de la cámara
        _, fotograma = captura.read()
        
        # Obtener la región horizontal de la imagen (1/3 de la altura)
        altura, ancho, _ = fotograma.shape
        region_horizontal = fotograma[altura//3:2*altura//3, :]
        
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
            cv2.rectangle(fotograma, (x, y + altura//3), (x + w, y + altura//3 + h), (0, 255, 0), 2)
        
        # Posicionar el texto en el centro de la región horizontal
        pos_x = 50
        pos_y = altura//3 + 50
        cv2.putText(fotograma, texto, (pos_x, pos_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Mostrar la imagen en una ventana
        cv2.imshow('Texto reconocido', fotograma)
        
        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar los recursos
    captura.release()
    cv2.destroyAllWindows()

            
reconocer_texto_camara()