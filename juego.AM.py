import pygame
import os
import random
import getpass


print("Please enter your new username:")
username = input()
print("Please enter your new password:")
password = getpass.getpass()
print(f"User {username} created successfully!")

pygame.init()

if os.path.exists('record.txt'):
    with open('record.txt', 'r') as f:
        tiempo_record = float(f.read())
else:
    tiempo_record = 0
ventana = pygame.display.set_mode((640,480))
pygame.display.set_caption("am")

jugando = False
tutorial = True
while not jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if tutorial:
                    tutorial = False
                else:
                    jugando = True

    ventana.fill((0, 0, 0))
    fuente = pygame.font.Font(None, 50)
    if tutorial:
        texto = fuente.render("Tutorial: Usa las flechas para moverte", True, (255, 255, 255))
        
    else:
        texto = fuente.render("Presiona ESPACIO para comenzar ", True, (255, 255, 255))
    ventana.blit(texto, (ventana.get_width() // 2 - texto.get_width() // 2,
                         ventana.get_height() // 2 - texto.get_height() // 2))
    pygame.display.flip()

ballrect = pygame.Rect(0, 0, 15, 15)  
speed = [3,3]
ballrect.move_ip(0,0)

baterect = pygame.Rect(0, 0, 120, 15)  
baterect.move_ip(240,450)

color_fondo = (0, 0, 255)  
color_pelota = (255, 255, 255)  

fuente = pygame.font.Font(None, 50)
texto = fuente.render("AM GAMES.cbtis 212,programacion", True, (255, 255, 255))  

vidas = 3
fuente_vidas = pygame.font.Font(None, 30)
texto_vidas = fuente_vidas.render("Vidas: " + str(vidas), True, (255, 255, 255))

fuente_tiempo = pygame.font.Font(None, 30)
tiempo_inicial = pygame.time.get_ticks()

nivel = 1
max_niveles = 10  
fuente_nivel = pygame.font.Font(None, 30)
texto_nivel = fuente_nivel.render("Nivel: " + str(nivel), True, (255, 255, 255))

pausado = False

power_ups = []
power_downs = []
power_up_timer = 0
power_down_timer = 0


power_ups_azul = []
power_downs_amarillo = []
power_up_azul_timer = 0
power_down_amarillo_timer = 0

puntuacion = 0
fuente_puntuacion = pygame.font.Font(None, 30)
texto_puntuacion = fuente_puntuacion.render("Puntuación: " + str(puntuacion), True, (255, 255, 255))

enemigos = []
enemigo_timer = 0

while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pausado = not pausado

    if pausado:
        continue

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        baterect = baterect.move(-3 * nivel,0)
    if keys[pygame.K_RIGHT]:
        baterect = baterect.move(3 * nivel,0)

    if baterect.colliderect(ballrect):
        speed[1] = -speed[1]

    ballrect = ballrect.move([i * nivel for i in speed])
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]
    if ballrect.bottom > ventana.get_height():
        speed[1] = -speed[1]
        vidas -= 1
        texto_vidas = fuente_vidas.render("Vidas: " + str(vidas), True, (255, 255, 255))
        if vidas == 0:
            print("Game over")
            jugando = False

    ventana.fill(color_fondo)
    
    pygame.draw.rect(ventana, color_pelota, ballrect)
    pygame.draw.rect(ventana, (255, 255, 255), baterect)  

   
    tiempo_actual = (pygame.time.get_ticks() - tiempo_inicial) / 1000
    texto_tiempo = fuente_tiempo.render("Tiempo: " + str(tiempo_actual), True, (255, 255, 255))
    
    
    if tiempo_actual // 25 > nivel - 1 and nivel < max_niveles:
        nivel += 1
        texto_nivel = fuente_nivel.render("Nivel: " + str(nivel), True, (255, 255, 255))
    
    if nivel == max_niveles and tiempo_actual // 25 > nivel:
        print("¡Felicidades, has completado todos los niveles!")
        jugando = False

    ventana.blit(texto_vidas,(10 ,10))
    ventana.blit(texto_tiempo,(ventana.get_width() - texto_tiempo.get_width() -10 ,10))
    ventana.blit(texto_nivel,(ventana.get_width() //2 - texto_nivel.get_width() //2, 10))
    ventana.blit(texto,(ventana.get_width() //2 - texto.get_width() //2,
                         ventana.get_height() //2 - texto.get_height() //2))

    power_up_timer += 1
    power_down_timer += 1
    if power_up_timer == 500:   
        power_up_timer = 0
        power_ups.append(pygame.Rect(random.randint(0, ventana.get_width()), 0, 10, 10))
    if power_down_timer == 1000:  
        power_down_timer = 0
        power_downs.append(pygame.Rect(random.randint(0, ventana.get_width()), 0, 10, 10))

    
    power_up_azul_timer += 1
    power_down_amarillo_timer += 1
    if power_up_azul_timer == 500:   
        power_up_azul_timer = 0
        power_ups_azul.append(pygame.Rect(random.randint(0, ventana.get_width()), 0, 10, 10))
    if power_down_amarillo_timer == 1000:  
        power_down_amarillo_timer = 0
        power_downs_amarillo.append(pygame.Rect(random.randint(0, ventana.get_width()), 0, 10, 10))

    for power_up in power_ups:
        power_up.move_ip(0, 1)
        if baterect.colliderect(power_up):
            power_ups.remove(power_up)
            baterect.inflate_ip(20, 0) 
    for power_down in power_downs:
        power_down.move_ip(0, 1)
        if baterect.colliderect(power_down):
            power_downs.remove(power_down)
            baterect.inflate_ip(-20, 0)  

    for power_up_azul in power_ups_azul:
        power_up_azul.move_ip(0, 1)
        if baterect.colliderect(power_up_azul):
            power_ups_azul.remove(power_up_azul)
            baterect.inflate_ip(20, 0) 
    for power_down_amarillo in power_downs_amarillo:
        power_down_amarillo.move_ip(0, 1)
        if baterect.colliderect(power_down_amarillo):
            power_downs_amarillo.remove(power_down_amarillo)
            

    enemigo_timer += 1
    if enemigo_timer == 700:  
        enemigo_timer = 0
        enemigos.append(pygame.Rect(random.randint(0, ventana.get_width()), 0, 10, 10))

    for enemigo in enemigos:
        enemigo.move_ip(0, 1)
        if baterect.colliderect(enemigo):
            enemigos.remove(enemigo)
            vidas -= 1  
            texto_vidas = fuente_vidas.render("Vidas: " + str(vidas), True, (255, 255, 255))
            if vidas == 0:
                print("Game over")
                jugando = False

    puntuacion = int(tiempo_actual * 10)  
    texto_puntuacion = fuente_puntuacion.render("Puntuación: " + str(puntuacion), True, (255, 255, 255))

    ventana.blit(texto_puntuacion,(ventana.get_width() - texto_puntuacion.get_width() -10 ,40))

    for power_up in power_ups:
        pygame.draw.rect(ventana, (0, 255, 0), power_up)  
    for power_down in power_downs:
        pygame.draw.rect(ventana, (255, 0, 0), power_down)  

    for power_up_azul in power_ups_azul:
        pygame.draw.rect(ventana, (0, 0, 255), power_up_azul)  
    for power_down_amarillo in power_downs_amarillo:
        pygame.draw.rect(ventana, (255, 255, 0), power_down_amarillo)  

    for enemigo in enemigos:
        pygame.draw.rect(ventana, (255, 0, 0), enemigo)  

    pygame.display.flip()
    pygame.time.Clock().tick(60)

if tiempo_actual > tiempo_record:
    with open('record.txt', 'w') as f:
        f.write(str(tiempo_actual))

pygame.quit()
