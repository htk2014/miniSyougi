import sys, pygame ,os,time

size = width, height = 800, 400
black = 0, 0, 0

koma_group = pygame.sprite.Group()

class Koma(pygame.sprite.Sprite):
          
	def __init__(self,img,nari_img,pos):
  
		pygame.sprite.Sprite.__init__(self,koma_group)

		self.width = 80
		self.height = 100

		self.front_image = pygame.image.load(img)
		self.front_image = pygame.transform.scale(self.front_image,(self.width,self.height)) 

		if nari_img == False:
			self.back_image = False
		else:
			self.back_image = pygame.image.load(nari_img)
			self.back_image = pygame.transform.scale(self.back_image,(self.width,self.height)) 


		self.posX = pos[0]
		self.posY = pos[1]

		self.image = self.front_image
		self.rect = self.image.get_rect() 
		self.rect.x = 280+(self.posX-1) * self.width
		self.rect.y = (self.posY-1) * self.height

		
	def turn(self):
		if self.back_image != False:
			if self.image == self.front_image:
				self.image = self.back_image
                  	else: self.image = self.front_image
	def getPos(self):	
		return [self.posX,self.posY]

	def posInit(self):	
		self.posX = False		
		self.posY = False		
		self.rect.x = False
		self.rect.y = False
	
	def move(self,pos):
		self.posX = pos[0]
		self.posY = pos[1]

		self.rect.x = 280+self.posX * self.width
		self.rect.y = self.posY * self.height

class Ban():
	def __init__(self,x,y):
		self.image = pygame.image.load("./img/mini_board3.jpg")
		self.image = pygame.transform.scale(self.image,(240,400)) 
		self.rect = self.image.get_rect() 
		self.rect.x = x
		self.rect.y = y

		#moti_kaku = Koma("./img/koma/kakuA.png",False,530,320)

		s_fu = Koma("./img/koma/fuA.png","./img/koma/nari_fuA.png",(2,3))
		s_kaku = Koma("./img/koma/kakuA.png",False,(1,4))
		s_hi = Koma("./img/koma/hiA.png",False,(3,4))
		s_ou = Koma("./img/koma/ouA.png",False,(2,4))

		g_fu = Koma("./img/koma/fuB.png","./img/koma/nari_fuB.png",(2,2))
		g_kaku = Koma("./img/koma/kakuB.png",False,(3,1))
		g_hi = Koma("./img/koma/hiB.png",False,(1,1))
		g_ou = Koma("./img/koma/ouB.png",False,(2,1))
		

		self.field = [
				[0,g_hi,g_ou,g_kaku,0],
				[0,0,g_fu,0,0],
				[0,0,0,0,0],
				[0,0,s_fu,0,0],
				[0,s_kaku,s_ou,s_hi,0],
				[0,0,0,0,0]]
		print self.field

	def draw(self,screen):
		screen.blit(self.image, self.rect)

	def komaDraw(self,screen):
		for vlst in self.field:
			for obj in vlst:
				if obj != 0:
					screen.blit(obj.image, obj.rect)

	def komaMove(self,koma,newPos,motigoma):
		oldPos = koma.getPos()
		self.field[oldPos[1]][oldPos[0]] = 0

		if self.field[newPos[1]+1][newPos[0]+1] != 0:
			self.field[newPos[1]+1][newPos[0]+1].posInit()
			motigoma.add(self.field[newPos[1]+1][newPos[0]+1])

		self.field[newPos[1]+1][newPos[0]+1] = koma
		print self.field

class Motigoma():
	def __init__(self):
		self.koma_lst = ()
	def add(self,koma):
		self.koma_lst.append(koma)
	def komaDraw(self):	
		for koma in self.koma_lst:
			screen.blit(koma.image, (530,300))
			

def selectKoma():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()
                                 #turn card      
                                for koma in koma_group:
					if koma.rect.collidepoint(pos):
						return koma

def selectField():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()
				if pos[0] >= 280 and pos[0] < 520:
					posX = (pos[0] - 280) / 80
					posY = pos[1] / 100
					return [posX,posY]
def play(ban,motigoma):
	koma = selectKoma()
	pos = selectField()

	ban.komaMove(koma,pos,motigoma)
	koma.move(pos)
	
	
def main():
	pygame.init()
	screen = pygame.display.set_mode(size)
	ban= Ban(280,0)
	motigoma= Motigoma()
	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()
                                 #turn card      
                                for koma in koma_group:
					if koma.rect.collidepoint(pos):
						print koma.getPos()
						
		screen.fill(black)
		ban.draw(screen)
		#koma_group.draw(screen)
		ban.komaDraw(screen)
		pygame.display.update()

		play(ban,motigoma)

		time.sleep(0.3)

main()
