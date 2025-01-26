import cv2

# Nome da imagem
IMAGE_PATH = 'C:\\Users\\35196\OneDrive\Ambiente de Trabalho\\tese\PIC_code\pixel2GPS\polardist\\tes.png'

# Nome do arquivo de saída
MAP_FILE = 'map.txt'

# Referências (rótulos) na ordem em que o usuário deve clicar
POINT_LABELS = [
    "Centro",
    "3m 0°", "9m 0°",
    "3m 90°", "9m 90°",
    "3m 180°", "9m 180°",
    "3m 270°", "9m 270°"
]

# Lista para armazenar as coordenadas clicadas
clicked_points = []
# Índice atual de ponto que precisamos capturar
current_index = 0

def mouse_callback(event, x, y, flags, param):
    global clicked_points, current_index
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if current_index < len(POINT_LABELS):
            # Armazena o ponto
            clicked_points.append((x, y))
            print(f"Ponto '{POINT_LABELS[current_index]}' capturado em (x={x}, y={y})")
            current_index += 1
            
            # Se já capturamos todos, salvamos e encerramos
            if current_index == len(POINT_LABELS):
                save_points_to_file(clicked_points, MAP_FILE)
                print(f"Todos os pontos foram capturados. Arquivo '{MAP_FILE}' salvo.")
                print("Feche a janela para encerrar.")
        else:
            print("Todos os pontos já foram capturados. Feche a janela.")

def save_points_to_file(points, filename):
    """
    Salva as coordenadas em um arquivo texto, 
    cada linha contendo: label x y
    """
    with open(filename, 'w') as f:
        for label, (x, y) in zip(POINT_LABELS, points):
            f.write(f"{label} {x} {y}\n")

def main():
    global current_index
    
    # Carrega a imagem
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"Erro ao carregar a imagem: {IMAGE_PATH}")
        return
    
    # Cria janela e seta callback de mouse
    cv2.namedWindow("Selecione os pontos na ordem indicada")
    cv2.setMouseCallback("Selecione os pontos na ordem indicada", mouse_callback)
    
    print("Por favor, clique nos pontos na seguinte ordem:")
    for i, lbl in enumerate(POINT_LABELS):
        print(f"{i+1}) {lbl}")
    
    while True:
        # Mostra a imagem
        cv2.imshow("Selecione os pontos na ordem indicada", image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC para sair
            break
        if current_index == len(POINT_LABELS):
            # Se já finalizou a captura, podemos encerrar após ESC
            pass
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
