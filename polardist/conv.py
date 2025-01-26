import cv2
import math

# Mesmo caminho da imagem usada no createMap.py
IMAGE_PATH = 'C:\\Users\\35196\OneDrive\Ambiente de Trabalho\\tese\PIC_code\pixel2GPS\polardist\\tes.png'
MAP_FILE   = 'map.txt'

# Vamos manter a mesma ordem de leitura (mas a ordem dentro do arquivo já deve vir correta)
POINT_LABELS = [
    "Centro",
    "3m 0°", "9m 0°",
    "3m 90°", "9m 90°",
    "3m 180°", "9m 180°",
    "3m 270°", "9m 270°"
]

# Variáveis globais para armazenar as referências
ref_points = {}  # dicionário: label -> (x, y)
center = (0, 0)

# Vetor que define 0° (em pixels)
v0 = (0, 0)

# Fator de escala (pixels por metro) estimado (pode-se melhorar usando todas as 4 direções)
pixel_per_meter = 1.0

def load_points_from_file(filename):
    """
    Lê o arquivo map.txt e retorna um dicionário:
    {
      "Centro": (xC, yC),
      "3m 0°": (x1, y1),
      ...
    }
    """
    points_dict = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            # Formato esperado: Label x y
            label = " ".join(parts[:-2])  # Caso o label tenha espaços
            x = int(parts[-2])
            y = int(parts[-1])
            points_dict[label] = (x, y)
    return points_dict

def setup_references():
    """
    - Carrega do map.txt
    - Calcula:
      (a) Centro
      (b) Vetor 0° (v0) em pixels (do centro até o 9m 0°, por exemplo)
      (c) Fator pixel_per_meter (usando a distância do centro até 9m 0°)
    """
    global ref_points, center, v0, pixel_per_meter
    
    # Carrega as referências
    ref_points = load_points_from_file(MAP_FILE)
    
    # Extrai o centro
    center = ref_points["Centro"]
    
    # Vetor 0°: vamos usar a posição do "9m 0°" para ser a direção de 0°
    x9m0, y9m0 = ref_points["9m 0°"]
    v0 = (x9m0 - center[0], y9m0 - center[1])
    
    # Distância em pixels do centro até 9m 0°
    dist_pixels_9m0 = math.hypot(v0[0], v0[1])
    
    # Se quisermos ser mais robustos, poderíamos também usar os pontos 9m 90°, 9m 180°, 9m 270°
    # e fazer uma média das distâncias, mas aqui faremos direto com 9m 0°.
    pixel_per_meter = dist_pixels_9m0 / 9.0

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Quando clicarmos, calculamos distância e ângulo
        distance_m, angle_deg = convert_pixel_to_distance_angle(x, y)
        
        print(f"Clique em (x={x}, y={y}) -> Distância: {distance_m:.2f} m, Ângulo: {angle_deg:.2f}°")

def convert_pixel_to_distance_angle(px, py):
    """
    Dado um ponto (px, py) em pixels, retorna (distância_em_metros, ângulo_em_graus)
    - O ângulo será medido em relação ao vetor 'v0' (definido como 0°).
    - A distância é calculada usando pixel_per_meter.
    """
    # Vetor do centro até o ponto clicado
    vx = px - center[0]
    vy = py - center[1]
    
    # Distância em pixels do centro
    dist_pixels = math.hypot(vx, vy)
    # Converte pra metros
    dist_m = dist_pixels / pixel_per_meter
    
    # Precisamos do ângulo entre v0 e (vx, vy)
    # Se v0 = (v0x, v0y) e vClicado = (vx, vy),
    #   ângulo = atan2(det(v0, vClicado), dot(v0, vClicado))
    # onde det(a,b) = a.x*b.y - a.y*b.x
    # e   dot(a,b) = a.x*b.x + a.y*b.y
    v0x, v0y = v0
    dot = v0x * vx + v0y * vy
    det = v0x * vy - v0y * vx
    angle_rad = math.atan2(det, dot)
    angle_deg = math.degrees(angle_rad)
    
    # Ajuste para ficar no range [0, 360)
    if angle_deg < 0:
        angle_deg += 360
    
    return dist_m, angle_deg

def main():
    # Configura as referências lendo o map.txt
    setup_references()
    
    # Carrega a imagem
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"Erro ao carregar a imagem: {IMAGE_PATH}")
        return
    
    cv2.namedWindow("Clique para obter distância e ângulo")
    cv2.setMouseCallback("Clique para obter distância e ângulo", mouse_callback)
    
    print("Clique em qualquer ponto para ver a distância (m) e o ângulo (graus).")
    print("Pressione ESC para sair.")
    
    while True:
        cv2.imshow("Clique para obter distância e ângulo", image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
