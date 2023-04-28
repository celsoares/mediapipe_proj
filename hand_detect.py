import cv2
import mediapipe as mp
import time
import pickle
import os

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

fase=0
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5, max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Frame não lido")
      continue
    image=cv2.flip(image, 1)
    alt, lar, canais = image.shape
    
    #Desenhar o quadrado e escrever
    if fase==0:
      x = int((lar - 200) / 2)
      y = int((alt - 200) / 2)
      #image = cv2.circle(image, (int(lar/2),int(alt/2)), 20, (255,0,0), 2)
      image = cv2.rectangle(image, (x, y), (x + 200, y + 200), (0, 0, 255), 2)
      imagem=cv2.putText(image, "coloque a mao no centro do quadrado",(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    # Tratamento da imagem para melhorar performance
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    # apagar ficheiros de posicao
    if fase==0:
      try:
        os.remove("pos_current.pkl")
      except:
        pass
      try:
        os.remove("pos_ini.pkl")
      except:
        pass

    # Verificar se existe a mao e desenha-la
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        lista_marcas=[]
        for lm in hand_landmarks.landmark:
            cx, cy, cz = int(lm.x * lar), int(lm.y * alt), int(lm.z*100)
            lista_marcas.append([cx, cy, cz])

        #image=cv2.circle(image,(lista_marcas[9][0], lista_marcas[9][1]), 10, (0,255,0), 5)
        
        mz=[]
        if fase ==0:
        #Verifica se todos os pontos estão dentro do quadrado
          for x in lista_marcas:
            if x[0]<(lar-200)/2 or x[0]>lar-((lar-200)/2):
              break
            if x[1]<(alt-200)/2 or x[1]>alt-((alt-200)/2):
              break
            mz.append(abs(x[2]))
          else:
            media_z=sum(mz)/len(mz)
            print(media_z)
            if media_z>5 and media_z<5.5:
              with open ("pos_ini.pkl", "wb") as file:
                file.write(pickle.dumps(lista_marcas))
              fase=1
        
        #Grava os pontos da mão no ficheiro(Depois de passar o teste do quadrado)
        elif fase==1:
          print(len(lista_marcas))
          with open ("pos_current.pkl", "wb") as file:
              file.write(pickle.dumps(lista_marcas))

        else:
          print("ERRO! Não devia executar isto: fase=", fase)
    else:
      fase=0
    
    #Exibir a imagem
    cv2.imshow('Controlo Garra', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

