import cv2
import numpy as np
import math

# Função para calcular o ângulo com base no referencial personalizado
def calcular_angulo_personalizado(centro, eixo_x, eixo_y, ponto):
    vetor_ponto = np.array([ponto[0] - centro[0], ponto[1] - centro[1]])
    vetor_ponto_normalizado = vetor_ponto / np.linalg.norm(vetor_ponto)

    # Projeção no eixo X
    cos_theta = np.dot(vetor_ponto_normalizado, eixo_x)
    # Projeção no eixo Y
    sin_theta = np.dot(vetor_ponto_normalizado, eixo_y)

    angulo = math.atan2(sin_theta, cos_theta)  # Calcula o ângulo em radianos
    angulo_graus = math.degrees(angulo)
    return (angulo_graus + 360) % 360  # Garante um valor em [0, 360)

# Carregar a imagem
caminho_imagem = input("Digite o caminho da imagem: ")
imagem = cv2.imread(caminho_imagem)
if imagem is None:
    print("Imagem não encontrada! Verifique o caminho fornecido.")
    exit()

# Redimensionar a imagem para facilitar a visualização
largura = 800
altura = int(imagem.shape[0] * (800 / imagem.shape[1]))
imagem = cv2.resize(imagem, (largura, altura))

# Lista para armazenar os pontos
pontos = []

def clique_do_mouse(evento, x, y, flags, param):
    global pontos, eixo_x, eixo_y, referencia_pronta

    if evento == cv2.EVENT_LBUTTONDOWN:
        pontos.append((x, y))
        print(f"Ponto marcado: {len(pontos)} - Coordenadas: ({x}, {y})")

        if len(pontos) <= 5:
            cv2.circle(imagem, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(imagem, str(len(pontos)), (x + 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if len(pontos) == 5:
            # Calcular os vetores do sistema de coordenadas personalizado
            centro = np.array(pontos[0])
            ponto_0 = np.array(pontos[1])
            ponto_90 = np.array(pontos[2])

            # Eixo X: vetor do centro ao ponto 0 graus
            eixo_x = ponto_0 - centro
            eixo_x = eixo_x / np.linalg.norm(eixo_x)  # Normalizar

            # Eixo Y: vetor do centro ao ponto 90 graus
            eixo_y = ponto_90 - centro
            eixo_y = eixo_y / np.linalg.norm(eixo_y)  # Normalizar

            referencia_pronta = True
            print("Referencial configurado. Clique em qualquer ponto para calcular os ângulos.")

        elif len(pontos) > 5 and referencia_pronta:
            # Calcular o ângulo do ponto clicado no referencial personalizado
            centro = np.array(pontos[0])
            angulo = calcular_angulo_personalizado(centro, eixo_x, eixo_y, (x, y))
            print(f"Ângulo do ponto clicado: {angulo:.2f} graus")

cv2.namedWindow("Imagem")
cv2.setMouseCallback("Imagem", clique_do_mouse)

print("Instruções:")
print("1. Clique no centro.")
print("2. Clique no ponto de referência a 0 graus.")
print("3. Clique no ponto de referência a 90 graus.")
print("4. Clique no ponto de referência a 180 graus.")
print("5. Clique no ponto de referência a 270 graus.")
print("Após isso, você pode clicar em qualquer ponto para obter o ângulo relativo ao referencial personalizado.")

referencia_pronta = False

while True:
    cv2.imshow("Imagem", imagem)
    tecla = cv2.waitKey(1)
    if tecla == 27:  # Tecla ESC para sair
        break

cv2.destroyAllWindows()
