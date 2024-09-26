from cmath import atan
from csv import list_dialects
import pygame
from pygame.locals import QUIT
from random import randint
import math


class Bola:
    def __init__(self, raio, sx, sy, vx, vy,cor):
        self.raio = raio
        self.sx = sx
        self.sy = sy
        self.vx = vx
        self.vy = vy
        self.cor = cor


    def colisao_parede(self):
        if self.sx - self.raio < 0:
            self.vx = self.vx * -1 
            self.sx = self.raio
            
        if self.sx + self.raio > Largura:
            self.vx = self.vx * -1 
            self.sx=Largura-self.raio

        if self.sy - self.raio < 0:
            self.vy = self.vy * -1
            self.sy=self.raio

        if self.sy + self.raio > Altura:
            self.vy = self.vy * -1
            self.sy=Altura-self.raio
            
    def desenha_bola(self):
        pygame.draw.circle(tela ,self.cor, (self.sx ,self.sy), self.raio)
    
    def atualiza_posição(self):
        self.sx = self.sx + self.vx
        self.sy = self.sy + self.vy

def modulo_velocidade(vx,vy):
    v = math.sqrt(vx*vx+vy*vy)
    return v
def velocidade_centro_de_massa(v1,v2,r1,r2):
    massa_total=r1*r1+r2*r2
    vcm=(v1*r1*r1+v2*r2*r2)/massa_total
    return vcm

def distancia_entre_pontos(x1, y1, x2, y2):
	return math.hypot(x2 - x1, y2 - y1)

def distancia_entre_bolas(bola1, bola2):
	return distancia_entre_pontos(bola1.sx, bola1.sy, bola2.sx, bola2.sy)

def colisão_bola(bola1 ,bola2):
    if distancia_entre_bolas(bola1,bola2) <= bola1.raio+bola2.raio:

        angulo = math.atan2(bola2.sy - bola1.sy, bola2.sx - bola1.sx)
        distancia_entre_circunferencias = bola1.raio + bola2.raio - distancia_entre_bolas(bola1, bola2)

        ax = distancia_entre_circunferencias * math.cos(angulo)
        ay = distancia_entre_circunferencias * math.sin(angulo)

		# corrige a colição (separa os dois)
        bola1.sx -= ax
        bola1.sy -= ay
        bola2.sx += ax
        bola2.sy += ay
        #decompondo oa vetors em relação ao ponto de colisao
        v1=modulo_velocidade(bola1.vx, bola1.vy)
        alfa1 = math.atan2((bola2.sy-bola1.sy),(bola2.sx - bola1.sx))
        beta1 = math.atan2((bola1.vy),(bola1.vx)) 
        angulo1 =beta1-alfa1
        v1t = v1*math.sin(angulo1)
        v1pi= v1*math.cos(angulo1)

        v2=modulo_velocidade(bola2.vx, bola2.vy)
        alfa2 = math.atan2((bola2.sy-bola1.sy),(bola2.sx - bola1.sx))
        beta2 = math.atan2((bola2.vy),(bola2.vx)) 
        angulo2 =beta2-alfa2
        v2t = v2*math.sin(angulo2)
        v2pi= v2*math.cos(angulo2)

        #calculando a velocidade em pi apos a colisão
        vcmpi = velocidade_centro_de_massa( v1pi, v2pi,bola1.raio,bola2.raio)
        v1pi = 2*vcmpi-v1pi #v=(1+cr)vcm-vi
        v2pi = 2*vcmpi-v2pi

        #transformando os vetores para codernada x,y
        bola1.vx = v1pi*math.cos(alfa1) - v1t*math.sin(alfa1)
        bola1.vy = v1pi*math.sin(alfa1) + v1t*math.cos(alfa1)
        bola2.vx = v2pi*math.cos(alfa2) - v2t*math.sin(alfa2)
        bola2.vy = v2pi*math.sin(alfa2) + v2t*math.cos(alfa2)

    while (bola1.sx-bola2.sx)*(bola1.sx-bola2.sx)+(bola1.sy-bola2.sy)*(bola1.sy-bola2.sy)-1<=(bola1.raio+bola2.raio)*(bola1.raio+bola2.raio):
        bola1.sx+=bola1.vx
        bola1.sy+=bola1.vy
        bola2.sx+=bola1.vx
        bola2.sy+=bola1.vy
        
#configuração do ramanho da tela
Altura = 800
Largura = 800
#configuração da velocidade maxima inicial das bolas e o numero de bolas
velocidade=5
numero_de_bolas=15
tam_max=100
tam_min=20


pygame.init()

#bolas
lista_bolas = []

for i in range(numero_de_bolas):
    lista_bolas.append(Bola(randint(tam_min,tam_max), randint(50, Largura-50), randint(50, Altura-50) , randint(-velocidade,velocidade), randint(-velocidade, velocidade),(randint(0,255),randint(0,255),randint(0,255))))
 


tela = pygame.display.set_mode((Largura, Altura))
pygame.display.set_caption('simulador')
relogio = pygame.time.Clock()

while True:
    relogio.tick(120)
    tela.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    energia=0
    for bola in lista_bolas:
        bola.atualiza_posição()
        bola.colisao_parede()
        bola.desenha_bola()
        energia +=(bola.raio*bola.raio*(math.hypot(bola.vx, bola.vy) ** 2)) / 2
    print(energia)
    for i in range(numero_de_bolas):
        for j in range(numero_de_bolas-1-i):
            colisão_bola(lista_bolas[i], lista_bolas[i+1+j])
    
    
    pygame.display.update()
