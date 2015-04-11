import sys, pygame ,os,time,random

size = width, height = 800, 400
black = 0, 0, 0

koma_group = pygame.sprite.Group()

class Koma(pygame.sprite.Sprite):
          
	def __init__(self,front_img_lst,nari_img_lst,pos,name,owner):
  
		pygame.sprite.Sprite.__init__(self,koma_group)
		
		self.name = name
		self.owner = owner

		self.front_img_lst = front_img_lst
		self.nari_img_lst = nari_img_lst

		self.width = 80
		self.height = 100

		img = filter(lambda lst:lst[1] == self.owner ,self.front_img_lst)[0]
		self.front_image = pygame.image.load(img)
		self.front_image = pygame.transform.scale(self.front_image,(self.width,self.height)) 

		if nari_img == False:
			self.back_image = False
		else:
	
			nari_img = filter(lambda lst:lst[1] == self.owner ,self.nari_img_lst)[0]
			self.nari_image = pygame.image.load(nari_img)
			self.nari_image = pygame.transform.scale(self.back_image,(self.width,self.height)) 


		self.posX = pos[0]
		self.posY = pos[1]

		self.image = self.front_image
		self.rect = self.image.get_rect() 
		self.rect.x = 280+(self.posX-1) * self.width
		self.rect.y = (self.posY-1) * self.height

		
	def turn(self):
		if self.back_image != False:
			if self.image == self.front_image:
				self.image = self.nari_image
                 	else: self.image = self.front_image

	def ownerChange(self,owner_name):
		self.owner = owner_name
		self.imageSwitch()
		
	def imageSwitch(type):
		front_img = filter(lambda lst:lst[1] == self.owner ,self.front_img_lst)[0]
		front_img= pygame.transform.scale(front_img,(self.width,self.height)) 
		self.image = front_img

		nari_img = filter(lambda lst:lst[1] == self.owner ,self.front_img_lst)[0]
		nari_img = pygame.transform.scale(nari_img,(self.width,self.height)) 


	def getPos(self):	
		return [self.posX,self.posY]

	def posInit(self):	
		self.posX = -1		
		self.posY = -1		
		self.rect.x = -1
		self.rect.y = -1
	
	def posUpdate(self,pos):
		self.posX = pos[0] + 1
		self.posY = pos[1] + 1

		print [self.posX,self.posY]

		self.rect.x = 280+(self.posX - 1) * self.width
		self.rect.y = (self.posY - 1) * self.height

class Motigoma():
	def __init__(self,pos,value_lst):
		self.koma_lst = []
		self.posX = pos[0]
		self.posY = pos[1]
		self.valueX = value_lst[0]
		self.valueY = value_lst[1]


	def add(self,koma):
		self.koma_lst.append(koma)

	def komaDraw(self,screen):	
		i = 0
		j = 0
		print self.koma_lst
		for koma in self.koma_lst:
			
			koma.rect.x = self.posX+i*self.valueX
			koma.rect.y = self.posY-j*self.valueY

			screen.blit(koma.image, (self.posX+i*self.valueX,self.posY-j*self.valueY))
			if i % 2 == 0 and i>=2:
				i = 0
				j = j + 1
			else:i = i + 1

	def is_excist(self,koma):
		for k in self.koma_lst:
			if koma == k:
				return True
		return False

class Ban():
	def __init__(self,x,y):
		self.image = pygame.image.load("./img/mini_board3.jpg")
		self.image = pygame.transform.scale(self.image,(240,400)) 
		self.rect = self.image.get_rect() 
		self.rect.x = x
		self.rect.y = y

		#moti_kaku = Koma("./img/koma/kakuA.png",False,530,320)

		s_fu = Koma(
				[("./img/koma/fuA.png","player"),("./img/koma/fuB.png","cpu")]
				[("./img/koma/nari_fuA.png","player"),("./img/koma/nari_fuB.png","cpu")]
				,(2,3)
				,"s_fu"
				,"player")
		s_kaku = Koma(("./img/koma/kakuA.png",False
				,(1,4)
				,"s_kaku"
				,"player")
		s_hi = Koma("./img/koma/hiA.png",False,(3,4),"s_hi","player")
		s_ou = Koma("./img/koma/ouA.png",False,(2,4),"s_ou","player")

		g_fu = Koma("./img/koma/fuB.png","./img/koma/nari_fuB.png",(2,2),"g_fu","cpu")
		g_kaku = Koma("./img/koma/kakuB.png",False,(3,1),"g_kaku","cpu")
		g_hi = Koma("./img/koma/hiB.png",False,(1,1),"g_hi","cpu")
		g_ou = Koma("./img/koma/ouB.png",False,(2,1),"g_ou","cpu")
		

		self.field = [
				[0,0,0,0,0],
				[0,g_hi,g_ou,g_kaku,0],
				[0,0,g_fu,0,0],
				[0,0,s_fu,0,0],
				[0,s_kaku,s_ou,s_hi,0],
				[0,0,0,0,0]]

	def draw(self,screen):
		screen.blit(self.image, self.rect)


	def komaDraw(self,screen):
		for vlst in self.field:
			for obj in vlst:
				if obj != 0:
					screen.blit(obj.image, obj.rect)
					print obj.name
				else: print 0

	def komaDraw2(self,screen):
		i = 0
		j = 0
		for vlst in self.field:
			for obj in vlst:
				if obj != 0: 
					rectX = 280+ (i - 1) * obj.width
					rectY = (j - 1) * obj.height
					screen.blit(obj.image, (rectX,rectY))
				i = i+1
			i = 0
			j = j+1

	def komaMove(self,koma,newPos,motigoma,motigoma_select,woner_name):
		if motigoma_select == False:
			oldPos = koma.getPos()
			self.field[oldPos[1]][oldPos[0]] = 0

		if self.field[newPos[1]+1][newPos[0]+1] != 0:
			torigoma = self.field[newPos[1]+1][newPos[0]+1]

			print torigoma.name

			torigoma.posInit()
			torigoma.ownerChange(woner_name)

			motigoma.add(torigoma)
			koma_group.remove(torigoma)

		self.field[newPos[1]+1][newPos[0]+1] = koma

def selectKoma(motigoma):
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()
                                 #turn card      
                                for koma in koma_group:
					if koma.rect.collidepoint(pos):
						return koma
				for koma in motigoma.koma_lst:
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
	koma = selectKoma(motigoma)
	pos = selectField()
	print pos
	motigoma_select = False

	if motigoma.is_excist(koma):
		motigoma.koma_lst.remove(koma)	
		koma_group.add(koma)
		motigoma_select = True

	ban.komaMove(koma,pos,motigoma,motigoma_select)
	koma.posUpdate(pos)
	
	print ban.field

class gamePlayer:
	def __init__(self,motigoma):
		self.motigoma = motigoma

	def selectkoma(self,ban):
		pass

	def selectField(self,ban,motigoma_select):
		pass

	def play(self,ban):
		koma = self.selectKoma(ban)
		
		if self.motigoma.is_excist(koma):
			motigoma_select = True
		else:   motigoma_select = False

		pos = self.selectField(ban,motigoma_select)

		if motigoma_select:
			self.motigoma.koma_lst.remove(koma)	
			koma_group.add(koma)

		ban.komaMove(koma,pos,self.motigoma,motigoma_select)
		koma.posUpdate(pos)
	
		print ban.field

def collectKoma(owner_name,ban):
		koma_lst = []
		for vlst in ban.field:
			for koma in vlst:
				
				if koma!=0 and koma.owner == owner_name:
					koma_lst.append(koma)
		return koma_lst

def collectPos(ban,fn):
	pos_lst = []
	i = 0
	j = 0

	for vlst in ban:
		for val in vlst:
			if i>=1 and i<=3 and j>=1 and j <=4:
				if fn(val):
					pos_lst.append((i,j))
			i = i+ 1
		i = 0
		j = j + 1

	return pos_lst

class Human(gamePlayer):
	def __init__(self,motigoma):
		gamePlayer.__init__(self,motigoma)
		self.name = "player"

	def selectKoma(self,ban):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
		 		if event.type == pygame.MOUSEBUTTONUP:
		 			pos = pygame.mouse.get_pos()
						
					koma_lst = collectKoma("player",ban)
                               	 	 #turn card      
                        		for koma in koma_lst:
						if koma.rect.collidepoint(pos):
							return koma

					for koma in self.motigoma.koma_lst:
						if koma.rect.collidepoint(pos):
							return koma
	def selectField(self,ban,motigoma_select):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
			 	if event.type == pygame.MOUSEBUTTONUP:
			 		pos = pygame.mouse.get_pos()
					if pos[0] >= 280 and pos[0] < 520:
						posX = (pos[0] - 280) / 80
						posY = pos[1] / 100

						if motigoma_select == False:
							#collect pos that empty or cpu's koma excists
							pos_lst = collectPos(ban.field,lambda val:(val == 0) if isinstance(val,int) else val.owner =="cpu")
							#jjjprint (posX+1,posY+1)
							#print pos_lst
							
						else:	
							#collect pos that empty
							pos_lst = collectPos(ban.field,lambda val:val == 0)

						if [] != filter(lambda lst:lst[0] == posX+1 and lst[1] == posY+1,pos_lst):
								return [posX,posY]

				
class Computer(gamePlayer):
	def __init__(self,motigoma):
		gamePlayer.__init__(self,motigoma)
		self.name = "cpu"
	
	def selectKoma(self):
		koma_lst = collectKoma("cpu",ban)
		rand_num = random.randint(0,len(koma_lst)-1)
		print rand_num

		return koma_lst[rand_num]

	def selectField(self,ban,motigoma_select):
		if motigoma_select == False:
			#collect pos that empty or cpu's koma excists
			pos_lst = collectPos(ban.field,lambda val:(val == 0) if isinstance(val,int) else val.owner =="player")
		else:	
			#collect pos that empty
			pos_lst = collectPos(ban.field,lambda val:val == 0)
		rand_num = random.randint(0,len(pos_lst))-1)

		return pos_lst[rand_num]

def main():
	pygame.init()
	screen = pygame.display.set_mode(size)
	ban = Ban(280,0)
	motigoma= Motigoma((530,300),(80,100))
	motigoma2= Motigoma((0,0),(80,-100))

	player = Human(motigoma)
	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()
                                 #turn card      
		screen.fill(black)
		ban.draw(screen)
		#ban.komaDraw(screen)
		#ban.komaDraw2(screen)
		motigoma.komaDraw(screen)
		koma_group.draw(screen)
		pygame.display.update()

		#play(ban,motigoma)
		player.play(ban)

		time.sleep(0.3)

main()
