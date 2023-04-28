import pickle
import serial
import PySimpleGUI as sg
import time
import math

#Calculo de distancia entre 2 pontos
def dist(x1, y1, x2, y2):
    dx = x1-x2
    dy = y1-y2
    d = math.sqrt(dx*dx + dy*dy)
    return int(d)

#M1_ini; M1_curr; M1_calc; M1_vel

layout=[[sg.Text("Posição inicial"), sg.Image("hand.png", size=(386,135))],
        [sg.Text("Motor1:"),sg.Text("", key="M1_ini", background_color="blue"),sg.Text("", key="M1_curr", background_color="blue"), sg.Text("", key="M1_calc", background_color="blue"), sg.Text("", key="M1_vel", background_color="blue")],
        [sg.Text("Motor2:"),sg.Text("", key="M2_ini", background_color="blue"),sg.Text("", key="M2_curr", background_color="blue"), sg.Text("", key="M2_calc", background_color="blue"), sg.Text("", key="M2_vel", background_color="blue")],
        [sg.Text("Motor3:"),sg.Text("", key="M3_ini", background_color="blue"),sg.Text("", key="M3_curr", background_color="blue"), sg.Text("", key="M3_calc", background_color="blue"), sg.Text("", key="M3_vel", background_color="blue")],
        [sg.Text("Motor4:"),sg.Text("", key="M4_ini", background_color="blue"),sg.Text("", key="M4_curr", background_color="blue"), sg.Text("", key="M4_calc", background_color="blue"), sg.Text("", key="M4_vel", background_color="blue")],
        [sg.Text("Motor5:"),sg.Text("", key="M5_ini", background_color="blue"),sg.Text("", key="M5_curr", background_color="blue"), sg.Text("", key="M5_calc", background_color="blue"), sg.Text("", key="M5_vel", background_color="blue")],
        [sg.Text("Motor6:"),sg.Text("", key="M6_ini", background_color="blue"),sg.Text("", key="M6_curr", background_color="blue"), sg.Text("", key="M6_calc", background_color="blue"), sg.Text("", key="M6_vel", background_color="blue")],
        [sg.Button("Ler"), sg.Button("SAIR")],
        [sg.Text("", key="info1", background_color="Red")],
        [sg.Text("", key="info2", background_color="Red")]]


janela = sg.Window("Controlo Garra", layout)

while True:
    
    event, values = janela.read(timeout=0)
    if event == sg.WIN_CLOSED  or event=="SAIR":
        break
#############################################################################
#       Ler os ficheiros
#############################################################################
    try:
        with open("pos_current.pkl", "rb") as file:
            curr = pickle.loads(file.read())
            janela["info2"].update("Posição corrente lida com sucesso!")
    except: 
        curr = []
        janela["info2"].update("Sem Controlo Detetado")
    
    try:
        with open("pos_ini.pkl", "rb") as file:
            ini = pickle.loads(file.read())
            janela["info1"].update("Posição Inicial lida com sucesso!")
    except: 
        ini = []
        janela["info1"].update("Sem Controlo Detetado")
        send="H"
    
    # - MOTOR1
    # - Ponto 9da mao: deslocação no eixo do x
    if len(ini)!=0:
        janela["M1_ini"].update(ini[9][0])
    else:
        janela["M1_ini"].update("")
    if len(curr)!=0:
        janela["M1_curr"].update(curr[9][0])
    else:
        janela["M1_curr"].update("")
    
    try:
        dif=ini[9][0]-curr[9][0]
        janela["M1_calc"].update(dif)
        if dif in range(-20, 20): vel=0
        elif dif in range(20, 60): vel=1
        elif dif in range(60, 120): vel=2
        elif dif >=120: vel=3
        elif dif in range(-60, -20): vel=4
        elif dif in range(-120, -60): vel=5
        elif dif<=-120: vel=6 
        janela["M1_vel"].update(vel)          
    except:
        janela["M1_calc"].update("")
        janela["M1_vel"].update("")
    
    # - MOTOR2
    # - Ponto 9da mao: deslocação no eixo do y
    if len(ini)!=0:
        janela["M2_ini"].update(ini[9][1])
    else:
        janela["M2_ini"].update("")
    if len(curr)!=0:
        janela["M2_curr"].update(curr[9][1])
    else:
        janela["M2_curr"].update("")
    
    try:
        dif=ini[9][1]-curr[9][1]
        janela["M2_calc"].update(dif)
        if dif in range(-20, 20): vel=0
        elif dif in range(20, 60): vel=1
        elif dif in range(60, 100): vel=2
        elif dif >=100: vel=3
        elif dif in range(-60, -20): vel=4
        elif dif in range(-100, -60): vel=5
        elif dif<=-100: vel=6 
        janela["M2_vel"].update(vel)          
    except:
        janela["M2_calc"].update("")
        janela["M2_vel"].update("")

    # - MOTOR3
    # - Ponto 1 e 12 da mao: diferença da posição z dos 2 pontos

    if len(ini)!=0:
        janela["M3_ini"].update(ini[12][2]-ini[1][2])
    else:
        janela["M3_ini"].update("")
    
    if len(curr)!=0:
        janela["M3_curr"].update(curr[12][2]-curr[1][2])
    else:
        janela["M3_curr"].update("")
    
    try:
        dif=(ini[12][2]-curr[1][2])-(curr[12][2]-curr[1][2])
        janela["M3_calc"].update(dif)
        if dif in range(-2, 2): vel=0
        elif dif in range(2, 6): vel=1
        elif dif in range(6, 10): vel=2
        elif dif >=10: vel=3
        elif dif in range(-6, -2): vel=4
        elif dif in range(-10, -6): vel=5
        elif dif<=-10: vel=6 
        janela["M3_vel"].update(vel)          
    except:
        janela["M3_calc"].update("")
        janela["M3_vel"].update("")

    # - MOTOR4
    # - Ponto 12 e 1 da mao: diferença da posição x dos 2 pontos

    if len(ini)!=0:
        janela["M4_ini"].update(ini[12][0]-ini[1][0])
    else:
        janela["M4_ini"].update("")
    
    if len(curr)!=0:
        janela["M4_curr"].update(curr[12][0]-curr[1][0])
    else:
        janela["M4_curr"].update("")
    
    try:
        dif=(ini[12][0]-ini[1][0])-(curr[12][0]-curr[1][0])
        janela["M4_calc"].update(dif)
        if dif in range(-30, 30): vel=0
        elif dif in range(30, 60): vel=1
        elif dif in range(60, 100): vel=2
        elif dif >=100: vel=3
        elif dif in range(-60, -30): vel=4
        elif dif in range(-100, -60): vel=5
        elif dif<=-100: vel=6
        janela["M4_vel"].update(vel)          
    except:
        janela["M4_calc"].update("")
        janela["M4_vel"].update("")
    
    # - MOTOR5
    # - Ponto 12 e 9 da mao: diferença da distancia dos 2 pontos
    #Posição Inicial corresponde à velocidade 6

    if len(ini)!=0:

        janela["M5_ini"].update(dist(ini[12][0],ini[12][1],ini[9][0],ini[9][1]))
    else:
        janela["M5_ini"].update("")
    
    if len(curr)!=0:
        janela["M5_curr"].update(dist(curr[12][0],curr[12][1],curr[9][0],curr[9][1]))
    else:
        janela["M5_curr"].update("")

    try:
        dif=dist(ini[12][0],ini[12][1],ini[9][0],ini[9][1])-dist(curr[12][0],curr[12][1],curr[9][0],curr[9][1])
        janela["M5_calc"].update(dif)
        if dif<5: vel=6
        elif dif<15: vel=5
        elif dif<25: vel=4
        elif dif<35: vel=0
        elif dif<45: vel=1
        elif dif<55: vel=2
        elif dif>55: vel=3
        janela["M5_vel"].update(vel)          
    except:
        janela["M5_calc"].update("")
        janela["M5_vel"].update("")

    # - MOTOR6 (GARRA)
    # - Ponto 8 e 4: Distancia entre os 2 pontos

    time.sleep(0.1)

janela.close()


# ser = serial.Serial('COM1', 9600)
# ser.flushInput()

# # Envie a string pela porta serial
# mensagem = "Olá mundo!"
# ser.write(mensagem.encode())

# # Feche a porta serial
# ser.close()






