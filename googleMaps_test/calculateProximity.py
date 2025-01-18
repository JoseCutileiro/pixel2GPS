import math

# Coordenadas originais e calculadas
original = (38.752862906669705, -9.184258581167594)
calculado = (38.75285042860869, -9.184242357938938)

# Função para calcular a distância haversine
def haversine(coord1, coord2):
    R = 6371000  # Raio da Terra em metros
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

# Calcular a distância
distancia_metros = haversine(original, calculado)
print(distancia_metros)
