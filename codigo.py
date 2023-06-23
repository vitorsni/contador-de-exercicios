import cv2
import mediapipe as mp
import math
from PySimpleGUI import PySimpleGUI as sg

def agachamento(url, quantidade, mostrar_pontos):
    #capturar video ou webcam
    video = cv2.VideoCapture(url)

    #popula a biblioteca de poses do mediapipe
    poseSolution = mp.solutions.pose

    #variavel para detectar movimento
    poseDetection = poseSolution.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)

    #desenhar as linhas e os pontos nos videos
    draw = mp.solutions.drawing_utils

    #contador de movimentos
    contador = 0

    #variavel para checar se o exercicio foi executado corretamente
    check = True

    #calorias por execucao
    cal_por_execucao = 0.2

    #variavel auxiliar pra saber quanto se abaixou
    maxDistanciaEsquerdo = 0

    #variavel auxiliar pra saber quanto se abaixou
    maxDistanciaDireito = 0

    #executa até que a quantidade solicitada for atingida
    while quantidade > contador:
        #le o video
        _,img = video.read()

        #converte o video em rgb
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        #detecta os pontos do corpo
        results = poseDetection.process(videoRGB)

        #coordenadas do corpo
        points = results.pose_landmarks

        #se estiver habilitado desenha os pontos e linhas na imagem
        if(mostrar_pontos):
            draw.draw_landmarks(img,points,poseSolution.POSE_CONNECTIONS)
        
        #pega tamanho da imagem
        h,w,_ = img.shape

        #só executa se reconhecer os pontos da pessoa
        if points:
            #pega a localização de cada ponto
            #cintura lado direito x e y
            cinturaDireitoY = int(points.landmark[poseSolution.PoseLandmark.RIGHT_HIP].y*h)
            cinturaDireitoX = int(points.landmark[poseSolution.PoseLandmark.RIGHT_HIP].x*w)

            #cintura lado esquerdo x e y
            cinturaEsquerdoY = int(points.landmark[poseSolution.PoseLandmark.LEFT_HIP].y*h)
            cinturaEsquerdoX = int(points.landmark[poseSolution.PoseLandmark.LEFT_HIP].x*w)

            #joelho direito x e y
            joelhoDireitoY = int(points.landmark[poseSolution.PoseLandmark.RIGHT_KNEE].y*h)
            joelhoDireitoX = int(points.landmark[poseSolution.PoseLandmark.RIGHT_KNEE].x*w)

            #joelho esquerdo x e y
            joelhoEsquerdoY = int(points.landmark[poseSolution.PoseLandmark.LEFT_KNEE].y*h)
            joelhoEsquerdoX = int(points.landmark[poseSolution.PoseLandmark.LEFT_KNEE].x*w)

            #distancia mao
            distanciaLadoEsquerdo = math.hypot(joelhoEsquerdoX-cinturaEsquerdoX,joelhoEsquerdoY-cinturaEsquerdoY)

            if(maxDistanciaEsquerdo < distanciaLadoEsquerdo):
                maxDistanciaEsquerdo = distanciaLadoEsquerdo

            #distancia pe
            distanciaLadoDireito = math.hypot(joelhoDireitoX-cinturaDireitoX,joelhoDireitoY-cinturaDireitoY)

            if(maxDistanciaDireito < distanciaLadoDireito):
                maxDistanciaDireito = distanciaLadoDireito
            #print(f'le {distanciaLadoEsquerdo} ld {distanciaLadoDireito}')
           

            #verifica se o exercicio foi feito 
            if check == True and distanciaLadoEsquerdo < (maxDistanciaEsquerdo - maxDistanciaEsquerdo * 0.3) and distanciaLadoDireito < (maxDistanciaDireito - distanciaLadoDireito * 0.3):
                contador +=1
                check = False
            
            #verifica se voltou pra pos inicial
            if distanciaLadoEsquerdo > (maxDistanciaEsquerdo - maxDistanciaEsquerdo * 0.1) and distanciaLadoDireito > (maxDistanciaDireito - distanciaLadoDireito * 0.1):
                check = True

            #mostra um texto na tela contendo a quantidade de execucoes e quantas calorias foram gastas
            cv2.putText(img,"Agachamento",(15,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)
            texto = f'Quantidade: {contador}'
            cv2.putText(img,texto,(15,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)
            texto = f'Calorias: {round(cal_por_execucao*contador, 2)}'
            cv2.putText(img,texto,(15,110),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)

        #mostra a imagem
        cv2.imshow('Acompanhamento',img)
        cv2.waitKey(1)
    return quantidade * cal_por_execucao

def polichinelo(url, quantidade, mostrar_pontos):
    #capturar video ou webcam
    video = cv2.VideoCapture(url)

    #popula a biblioteca de poses do mediapipe
    poseSolution = mp.solutions.pose

    #variavel para detectar movimento
    poseDetection = poseSolution.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)

    #desenhar as linhas e os pontos nos videos
    draw = mp.solutions.drawing_utils

    #contador de movimentos
    contador = 0

    #variavel para checar se o exercicio foi executado corretamente
    check = True

    #calorias por execucao
    cal_por_execucao = 0.2

    #executa até que a quantidade solicitada for atingida
    while quantidade > contador:
        #le o video
        _,img = video.read()

        #converte o video em rgb
        videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        #detecta os pontos do corpo
        results = poseDetection.process(videoRGB)

        #coordenadas do corpo
        points = results.pose_landmarks

        #se estiver habilitado desenha os pontos e linhas na imagem
        if(mostrar_pontos):
            draw.draw_landmarks(img,points,poseSolution.POSE_CONNECTIONS)
        
        #pega tamanho da imagem
        h,w,_ = img.shape

        #só executa se reconhecer os pontos da pessoa
        if points:
            #pega a localização de cada ponto
            #pé direito x e y
            peDireitoY = int(points.landmark[poseSolution.PoseLandmark.RIGHT_FOOT_INDEX].y*h)
            peDireitoX = int(points.landmark[poseSolution.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

            #pé esquerdo x e y
            peEsquerdoY = int(points.landmark[poseSolution.PoseLandmark.LEFT_FOOT_INDEX].y*h)
            peEsquerdoX = int(points.landmark[poseSolution.PoseLandmark.LEFT_FOOT_INDEX].x*w)

            #mão direita x e y
            maoDireitaY = int(points.landmark[poseSolution.PoseLandmark.RIGHT_INDEX].y*h)
            maoDireitaX = int(points.landmark[poseSolution.PoseLandmark.RIGHT_INDEX].x*w)

            #mão esquerda x e y
            maoEsquerdaY = int(points.landmark[poseSolution.PoseLandmark.LEFT_INDEX].y*h)
            maoEsquerdaX = int(points.landmark[poseSolution.PoseLandmark.LEFT_INDEX].x*w)

            #distancia mao
            distanciaMao = math.hypot(maoDireitaX-maoEsquerdaX,maoDireitaY-maoEsquerdaY)
            #distancia pe
            distanciaPe = math.hypot(peDireitoX-peEsquerdoX,peDireitoY-peEsquerdoY)

            #verifica se o exercicio foi feito 
            if check == True and distanciaMao <=150 and distanciaPe >=150:
                contador +=1
                check = False

            #verifica se voltou pra pos inicial
            if distanciaMao >150 and distanciaPe <150:
                check = True

            #mostra um texto na tela contendo a quantidade de execucoes e quantas calorias foram gastas
            cv2.putText(img,"Polichinelo",(15,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)
            texto = f'Quantidade: {contador}'
            cv2.putText(img,texto,(15,80),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)
            texto = f'Calorias: {round(cal_por_execucao*contador, 2)}'
            cv2.putText(img,texto,(15,110),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),5)

        #mostra a imagem
        cv2.imshow('Acompanhamento',img)
        cv2.waitKey(1)
    return quantidade * cal_por_execucao

#Layout

#definição do tema da aplicação
sg.theme('Reddit')

#variavel das calorias gastas
calorias = 0

#definição da parte superior da tela
telaCima= [
    [sg.Text('Acompanhamento Fitness', font=("arial", 22))],
    [sg.Text('Acompanhe seus exercícios com a ajuda da tecnologia!', font=("arial", 14))],
    [sg.Text('', font=("arial", 12))],
    [sg.Text('Determine a quantidade de cada exercicio que deseja fazer', font=("arial", 12))],
    [sg.Text('Você também pode ativar os identificadores para entender como funciona', font=("arial", 12))],
    [sg.Text('', font=("arial", 12))],
]
#definição da parte central da tela
telaCentro= [
    [sg.Checkbox('Mostrar identificadores?', key='linhas', font=("arial", 12))],
    [sg.Text('Quantidade de polichinelos:     ', font=("arial", 12)), sg.Input(key='num_plc', size=(4,1))],
    [sg.Text('Quantidade de agachamentos:', font=("arial", 12)), sg.Input(key='num_agc', size=(4,1))],
    [sg.Text(f'Você ja gastou {calorias} calorias!', font=("arial", 12), text_color= "green", key= 'caloriasText')],
    [sg.Text('', font=("arial", 12))],
]
#definição da parte interior da tela
telaFim= [
    [sg.Button('Exercitar!', font=("arial", 12),size= (50,50)), sg.Button('Vídeo de exemplo', font=("arial", 12),size= (10,50))]
]

#definição do layout da tela, unindo todas as definições de tela
layout = [[sg.VPush()],
              [sg.Push(), sg.Column(telaCima, element_justification='center'), sg.Push()],
              [sg.Column(telaCentro, element_justification='left'), sg.Push()],
              [sg.Push(), sg.Column(telaFim, element_justification='center'), sg.Push()],
              [sg.VPush()]]

#Janela
janela= sg.Window('Acompanhamento Fitness v1.0', layout, size=(600,410))

#Ler os eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    if eventos == 'Exercitar!':
        try:
            valor_plc = int(valores['num_plc'])
        except:
            sg.popup("O valor do campo 'Quantidade de polichinelos' não é válido!", title= "Advertência")
            janela['num_plc'].Update('')
            continue

        try:
            valor_agc = int(valores['num_agc'])
        except:
            sg.popup("O valor do campo 'Quantidade de agachamentos' não é válido!", title= "Advertência")
            janela['num_agc'].Update('')
            continue

        if valor_plc > 0:
            sg.popup("Se posicione e confirme quando estiver pronto!",title= "Se Posicione")
            calAtual = polichinelo(0, valor_plc, valores['linhas'])
            calorias = calorias + calAtual
            janela['caloriasText'].Update(f'Você ja gastou {calorias} calorias!')
            cv2.destroyWindow("Acompanhamento")
            sg.popup(f"Parabéns, você conseguiu e gastou {calAtual} calorias!",title= "Sucesso")
        if valor_agc > 0:
            sg.popup("Se posicione e confirme quando estiver pronto!",title= "Se Posicione")
            calAtual = agachamento(0, valor_agc, valores['linhas'])
            calorias = calorias + calAtual
            janela['caloriasText'].Update(f'Você ja gastou {calorias} calorias!')
            cv2.destroyWindow("Acompanhamento")
            sg.popup(f"Parabéns, você conseguiu e gastou {calAtual} calorias!",title= "Sucesso")
        if valor_agc < 1 and valor_plc < 1:
            sg.popup("Você precisa estar com pelo menos uma quantidade positiva nos campos!")
    if eventos == 'Vídeo de exemplo':
        calAtual = 0
        sg.popup("Acompanhe o exemplo de agachamento com 5 execuções!",title= "Exemplo")
        calAtual = calAtual + agachamento("agachamentoEx.mp4", 3, True)
        cv2.destroyWindow("Acompanhamento")
        sg.popup("Acompanhe o exemplo de polichinelo com 5 execuções!",title= "Exemplo")
        calAtual = calAtual + polichinelo("polichineloEx.mp4", 3, True)
        cv2.destroyWindow("Acompanhamento")
        sg.popup(f"Você acompanhou o vídeo exemplo de como funciona nosso sistema e o personagem gastou {round(calAtual, 2)} calorias.",title= "Exemplo")