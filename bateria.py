import cv2
from djitellopy import Tello

def main():
    # Inicializa o drone Tello
    tello = Tello()

    # Conecta-se ao drone
    tello.connect()

    # Verifica o estado da bateria do drone
    print(f"Nivel da bateria: {tello.get_battery()}%")

    # Inicia a transmissão de vídeo
    tello.streamon()

    while True:
        # Captura uma imagem da câmera do Tello
        frame = tello.get_frame_read().frame

        # Exibe a imagem capturada
        cv2.imshow("Tello Camera", frame)

        # Condição para parar o loop (pressione 'q' para sair)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera os recursos
    cv2.destroyAllWindows()
    tello.streamoff()

if __name__ == "__main__":
    main()