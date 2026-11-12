from djitellopy import Tello
import time

# Cria uma instância do drone
tello = Tello()

# Conecta-se ao Tello
tello.connect()

# Tenta acessar a IMU
try:
    #imu_data = tello.get_imu()
    #print(f"IMU data: {imu_data}")
    battery_level =  tello.get_battery()
    print(f"Battery: {battery_level}")
except Exception as e:
    print(f"Erro ao acessar IMU: {e}")

# Você pode executar os outros comandos do drone aqui

tello.send_command_with_return('takeoff')
time.sleep(1)
tello.send_command_with_return('forward 120')
time.sleep(4)
tello.send_command_with_return('land')

