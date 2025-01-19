import matplotlib.pyplot as plt
import numpy as np
from matplotlib.image import imread

# Carregar a imagem
img = imread('img.jpeg')

# Variáveis globais para armazenar os pontos
points = []
center = None
x_axis = None

# Função para calcular ângulo em relação ao centro e ao eixo x
def calculate_angle(center, x_axis, point):
    vector_center_to_point = np.array([point[0] - center[0], point[1] - center[1]])
    vector_center_to_xaxis = np.array([x_axis[0] - center[0], x_axis[1] - center[1]])

    # Normalizar os vetores
    norm_point = vector_center_to_point / np.linalg.norm(vector_center_to_point)
    norm_xaxis = vector_center_to_xaxis / np.linalg.norm(vector_center_to_xaxis)

    # Calcular o ângulo (em radianos) e converter para graus
    angle_rad = np.arccos(np.clip(np.dot(norm_point, norm_xaxis), -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)

    # Determinar o lado do eixo (direita ou esquerda)
    cross_product = np.cross(vector_center_to_xaxis, vector_center_to_point)
    if cross_product < 0:
        angle_deg = 360 - angle_deg

    return angle_deg

# Callback para capturar cliques
def onclick(event):
    global points, center, x_axis

    if event.xdata is None or event.ydata is None:
        return  # Clique fora da área da imagem

    # Registrar ponto clicado
    points.append((event.xdata, event.ydata))

    if len(points) <= 5:
        print(f"Ponto {len(points)} registrado em: ({event.xdata:.2f}, {event.ydata:.2f})")
        if len(points) == 1:
            center = points[0]
            print("Centro definido.")
        elif len(points) == 2:
            x_axis = points[1]
            print("Eixo X definido.")
    else:
        # Calcular o ângulo em relação ao centro e ao eixo x
        angle = calculate_angle(center, x_axis, (event.xdata, event.ydata))
        print(f"Ângulo do ponto clicado: {angle:.2f} graus")

# Exibir a imagem
fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("Clique para marcar os pontos")

# Conectar o evento de clique
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
