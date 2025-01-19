import numpy as np
from scipy.interpolate import LinearNDInterpolator

# Dados dos ficheiros
pixels = [
    (741, 937),
    (966, 442),
    (1744, 339),
    (1845, 519)
]
gps_coordinates = [
    (38.7078639, -9.2987466),
    (38.7080407, -9.2988146),
    (38.7080585, -9.2987278),
    (38.7080070, -9.2987261)
]

test_pixel = (1235, 494)

# Separar os valores para interpolação
x_pixels, y_pixels = zip(*pixels)
latitudes, longitudes = zip(*gps_coordinates)

# Criar interpoladores para latitude e longitude
interpolator_lat = LinearNDInterpolator(pixels, latitudes)
interpolator_lon = LinearNDInterpolator(pixels, longitudes)

# Prever a posição GPS para o pixel de teste
test_latitude = interpolator_lat(test_pixel)
test_longitude = interpolator_lon(test_pixel)

if test_latitude is not None and test_longitude is not None:
    print(f"A posição GPS prevista para 'test.jpeg' é: {test_latitude:.7f}, {test_longitude:.7f}")
else:
    print("Não foi possível prever a posição GPS para 'test.jpeg'. Verifique os dados fornecidos.")
