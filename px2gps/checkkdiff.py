from geopy.distance import geodesic

def calcular_diferenca(cordenadas_originais, cordenadas_previstas):
    """
    Calcula a diferença em metros entre duas coordenadas GPS.

    Args:
        cordenadas_originais (tuple): Coordenadas GPS originais (latitude, longitude).
        cordenadas_previstas (tuple): Coordenadas GPS previstas (latitude, longitude).

    Returns:
        float: Diferença em metros entre as coordenadas.
    """
    return geodesic(cordenadas_originais, cordenadas_previstas).meters

if __name__ == "__main__":
    # Solicitar ao utilizador as coordenadas originais e previstas
    print("Digite as coordenadas originais (latitude e longitude, separados por vírgula):")
    originais_input = input("Exemplo: 38.7078639,-9.2987466\n")
    
    print("Digite as coordenadas previstas (latitude e longitude, separados por vírgula):")
    previstas_input = input("Exemplo: 38.7079000,-9.2988000\n")

    # Converter as entradas para tuplas de floats
    try:
        cordenadas_originais = tuple(map(float, originais_input.split(",")))
        cordenadas_previstas = tuple(map(float, previstas_input.split(",")))

        # Calcular a diferença em metros
        diferenca = calcular_diferenca(cordenadas_originais, cordenadas_previstas)
        print(f"A diferença entre as coordenadas é de {diferenca:.2f} metros.")

    except ValueError:
        print("Erro: Certifique-se de que inseriu valores numéricos separados por vírgula.")
