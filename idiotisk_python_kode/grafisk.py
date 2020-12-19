import sys, pygame
import math
pygame.init()
def mat_mul(Matrix,vector):
    out = [ 0 for i in vector]
    for i in range(len(out)):
        for j, el_j in enumerate(vector): 
            out[i] += Matrix[i][j]*el_j
    return out


M = [[1,0],[0,1]]
vec = [21,14]
new = mat_mul(M, vec)
print(new)







def main():
    size = width, height = 320*3, 240*3
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ball = pygame.transform.scale(pygame.image.load("Smiley.bmp"), (100,100))
    ballrect = ball.get_rect()
    rot_mat = [[math.cos(0.1), math.sin(0.1)], [ -math.sin(0.1), math.cos(0.1)]]
    print(rot_mat)
    ballrect = ballrect.move((100,100))
    current_pos = [ ballrect.left, ballrect.top]
    origin= [200,200]
    print(current_pos)    
    while 1:
        origin = [i+0.1 for i in origin]
        current_pos = [ ballrect.left- origin[0], ballrect.top- origin[1]]
        new_pos = mat_mul(rot_mat, current_pos)
        ballrect =ballrect.move((new_pos[0] -current_pos[0], new_pos[1]-current_pos[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
main()