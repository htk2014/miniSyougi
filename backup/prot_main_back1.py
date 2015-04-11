import sys, pygame ,os,time

size = width, height = 800, 400
black = 0, 0, 0

koma_group = pygame.sprite.Group()

class Koma(pygame.sprite.Sprite):
          
	def __init__(self,img,nari_img,posX,posY):
  
		pygame.sprite.Sprite.__init__(self,koma_group)

		self.width = 80
		self.height = 80

		self.front_image = pygame.image.load(img)
		self.front_image = pygame.transform.scale(self.front_image,(self.width,self.height)) 

		if nari_img == False:
			self.back_image = False
		else:
			self.back_image = pygame.image.load(nari_img)
			self.back_image = pygame.transform.scale(self.back_image,(self.width,self.height)) 

		self.width = 50
		self.height = 75

		self.image = self.front_image
		self.rect = self.image.get_rect() 
		self.rect.x = 280+posX * 80
		self.rect.x = posX * 80

		self.posX = posX+1
		self.posY = posY+1

	def turn(self):
		if self.back_image != False:
			if self.image == self.front_image:
				self.image = self.back_image
                  	else: self.image = self.front_image


class Ban():
	def __init__(self,x,y):
		self.image = pygame.image.load("./img/mini_board2.jpg")
		self.image = pygame.transform.scale(self.image,(240,400)) 
		self.rect = self.image.get_rect() 
		self.rect.x = x
		self.rect.y = y

		#moti_kaku = Koma("./img/koma/kakuA.png",False,530,320)

		s_fu = Koma("./img/koma/fuA.png","./img/koma/nari_fuA.png",1,5)
		s_kaku = Koma("./img/koma/kakuA.png",False,0,6)
		s_hi = Koma("./img/koma/hiA.png",False,2,6)
		s_ou = Koma("./img/koma/ouA.png",False,1,6)

		self.field = [
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,0,0,0],
				[0,0,s_fu,0,0],
				[0,s_kaku,s_ou,s_hi,0],
				[0,0,0,0,0]]
		print self.field

	def draw(self,screen):
		screen.blit(self.image, self.rect)
def main():
	pygame.init()
	screen = pygame.display.set_mode(size)
	ban= Ban(280,0)
	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		screen.fill(black)
		ban.draw(screen)
		koma_group.draw(screen)
		pygame.display.update()
		time.sleep(0.3)

main()
