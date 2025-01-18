import cv2
import numpy as np

def pixel_to_gps(x, y, img_width, img_height, top_left_gps, bottom_right_gps):
    """
    Converte coordenadas de pixel para GPS.
    
    Args:
        x, y: Coordenadas do pixel.
        img_width, img_height: Dimensões da imagem.
        top_left_gps: Coordenadas GPS do canto superior esquerdo.
        bottom_right_gps: Coordenadas GPS do canto inferior direito.

    Retorna:
        latitude, longitude: Coordenadas GPS calculadas.
    """
    # Separar latitude e longitude das coordenadas dadas
    lat1, lon1 = top_left_gps
    lat2, lon2 = bottom_right_gps

    # Calcular frações de posição do pixel na imagem
    x_frac = x / img_width
    y_frac = y / img_height

    # Interpolar coordenadas GPS
    latitude = lat1 + y_frac * (lat2 - lat1)
    longitude = lon1 + x_frac * (lon2 - lon1)

    return latitude, longitude

def on_mouse_click(event, x, y, flags, params):
    """
    Callback do mouse para capturar cliques e exibir coordenadas GPS.
    """
    if event == cv2.EVENT_RBUTTONDOWN:  # Clique com o botão direito
        img, img_width, img_height, top_left_gps, bottom_right_gps = params
        gps_coords = pixel_to_gps(x, y, img_width, img_height, top_left_gps, bottom_right_gps)
        print(f"Coordenadas clicadas: Pixel ({x}, {y}) -> GPS {gps_coords}")

# Carregar imagem
image_path = input("Insira o caminho da imagem: ")
image = cv2.imread(image_path)

if image is None:
    print("Erro ao carregar a imagem. Verifique o caminho.")
    exit()

img_height, img_width, _ = image.shape

# Receber coordenadas GPS do usuário
print("Insira as coordenadas GPS dos cantos da imagem:")
try:
    top_left_gps = tuple(map(float, input("Canto superior esquerdo (latitude, longitude): ").split(',')))
    bottom_right_gps = tuple(map(float, input("Canto inferior direito (latitude, longitude): ").split(',')))
except ValueError:
    print("Erro: Insira as coordenadas no formato 'latitude,longitude'.")
    exit()

# Exibir imagem e configurar callback
cv2.imshow("Imagem", image)
cv2.setMouseCallback("Imagem", on_mouse_click, (image, img_width, img_height, top_left_gps, bottom_right_gps))

print("Clique com o botão direito na imagem para obter coordenadas GPS do ponto clicado.")

cv2.waitKey(0)
cv2.destroyAllWindows()