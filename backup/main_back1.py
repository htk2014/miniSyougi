import sys
import  pygame 
import os
import time
import random

size = width, height = 800, 400
black = 0, 0, 0

koma_group = pygame.sprite.Group()

class Koma(pygame.sprite.Sprite):
          
	def __init__(self,front_img_lst,dir_lst,pos,name,owner):
  
		pygame.sprite.Sprite.__init__(self,koma_group)
		
		self.name = name
		self.owner = owner

		self.dir_lst = dir_lst 

		self.width = 80
		self.height = 100

		self.nariFlag = False

		img = pygame.image.load(front_img_lst["player"])
		player_img = pygame.transform.scale(img,(self.width,self.height)) 

		img = pygame.image.load(front_img_lst["cpu"])
		cpu_img = pygame.transform.scale(img,(self.width,self.height)) 

		self.image_lst = {"player":player_img,"cpu":cpu_img}
		self.front_image = self.image_lst[self.owner]

		self.image = self.front_image

		self.posX = pos[0]
		self.posY = pos[1]

		self.rect = self.image.get_rect() 
		self.rect.x = 280+(self.posX-1) * self.width
		self.rect.y = (self.posY-1) * self.height
	
	def ownerChange(self,owner_name):
		self.owner = owner_name
		self.imageSwitch()
		
	def imageSwitch(self):
		self.front_image = self.image_lst[self.owner]
		self.image = self.front_image

	def getPos(self):	
		return [self.posX,self.posY]

	def posInit(self):	
		self.posX = -1		
		self.posY = -1		
		self.rect.x = -1
		self.rect.y = -1
	
	def posUpdate(self,pos):
		self.posX = pos[0]
		self.posY = pos[1]

		self.rect.x = 280+(self.posX - 1) * self.width
		self.rect.y = (self.posY - 1) * self.height

class Ou(Koma):
	def __init__(self,front_img_lst,dir_lst,pos,name,owner):
		Koma.__init__(self,front_img_lst,dir_lst,pos,name,owner)
class Fu(Koma):
	def __init__(self,front_img_lst,nari_img_lst,special_dir_lst,nari_dir_lst,pos,name,owner):
		self.special_dir_lst = special_dir_lst
		dir_lst = self.special_dir_lst[owner]

		Koma.__init__(self,front_img_lst,dir_lst,pos,name,owner)
		self.nari_dir_lst = nari_dir_lst

		img = pygame.image.load(nari_img_lst["player"])
		player_nari_img = pygame.transform.scale(img,(self.width,self.height)) 

		img = pygame.image.load(nari_img_lst["cpu"])
		cpu_nari_img = pygame.transform.scale(img,(self.width,self.height)) 

		self.nari_image_lst = {"player":player_nari_img,"cpu":cpu_nari_img}
		
		self.nari_image = self.nari_image_lst[self.owner]
		
	def turn(self):
		if self.image == self.front_image:
			self.image = self.nari_image
               	else: self.image = self.front_image
	
	def nari(self):
		self.nariFlag = True
		self.turn()
		self.dir_lst = self.nari_dir_lst
		
	def imageSwitch(self):
		self.front_image = self.image_lst[self.owner]
		self.image = self.front_image

		self.nari_image = self.nari_image_lst[self.owner] 

	def dirChange(self):
		self.dir_lst = self.special_dir_lst[self.owner]

	def ownerChange(self,owner_name):
		self.owner = owner_name
		self.imageSwitch()
		self.dirChange()
		self.nariFlag = False

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

		for koma in self.koma_lst:
			
			koma.rect.x = self.posX+i*self.valueX
			koma.rect.y = self.posY+j*self.valueY

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

		img = pygame.image.load("./img/light.png")
		self.light_image = pygame.transform.scale(img,(79,98)) 

		#moti_kaku = Koma("./img/koma/kakuA.png",False,530,320)

		fu_front_img_lst = {"player":"./img/koma/fuA.png","cpu":"./img/koma/fuB.png"}
		fu_nari_img_lst = {"player":"./img/koma/nari_fuA.png","cpu":"./img/koma/nari_fuB.png"}
		fu_dir = {"player":[(0,-1)],"cpu":[(0,1)]}
		fu_nari_dir = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1),(1,-1)]
		s_fu = Fu(fu_front_img_lst,fu_nari_img_lst,fu_dir,fu_nari_dir,(2,3),"s_fu","player")
		g_fu = Fu(fu_front_img_lst,fu_nari_img_lst,fu_dir,fu_nari_dir,(2,2),"g_fu","cpu")

		kaku_img_lst ={"player":"./img/koma/kakuA.png","cpu":"./img/koma/kakuB.png"}
		kaku_dir = [(-1,-1),(1,1),(-1,1),(1,-1)]
		s_kaku = Koma(kaku_img_lst,kaku_dir,(1,4),"s_kaku","player")
		g_kaku = Koma(kaku_img_lst,kaku_dir,(3,1),"g_kaku","cpu")

		hi_img_lst ={"player":"./img/koma/hiA.png","cpu":"./img/koma/hiB.png"}
		hi_dir = [(1,0),(-1,0),(0,1),(0,-1)]
		s_hi = Koma(hi_img_lst,hi_dir,(3,4),"s_hi","player")
		g_hi = Koma(hi_img_lst,hi_dir,(1,1),"g_hi","cpu")

		ou_img_lst ={"player":"./img/koma/ouA.png","cpu":"./img/koma/ouB.png"}
		ou_dir = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1),(1,-1)]
		s_ou = Ou(ou_img_lst,ou_dir,(2,4),"s_ou","player")
		g_ou = Ou(ou_img_lst,ou_dir,(2,1),"g_ou","cpu")
		
		self.field = [
				[0,0,0,0,0],
				[0,g_hi,g_ou,g_kaku,0],
				[0,0,g_fu,0,0],
				[0,0,s_fu,0,0],
				[0,s_kaku,s_ou,s_hi,0],
				[0,0,0,0,0]]

	def draw(self,screen):
		screen.blit(self.image, self.rect)

	def light_draw(self,screen,pos):
		rectX = 280+(pos[0] - 1) * 80
		rectY = (pos[1] - 1) * 100

		screen.blit(self.light_image, (rectX,rectY))

	def brightFiled(self,screen,pos_lst):
		for pos in pos_lst:
			self.light_draw(screen,pos)
		pygame.display.update()

	def komaMove(self,koma,newPos,motigoma,motigoma_flag,woner_name):
		if motigoma_flag == False:
			oldPos = koma.getPos()
			self.field[oldPos[1]][oldPos[0]] = 0

		if self.field[newPos[1]][newPos[0]] != 0:
			torigoma = self.field[newPos[1]][newPos[0]]

			torigoma.posInit()
			torigoma.ownerChange(woner_name)

			motigoma.add(torigoma)
			koma_group.remove(torigoma)
		else: torigoma = False

		self.field[newPos[1]][newPos[0]] = koma

		return torigoma

class gamePlayer:
	def __init__(self,name,motigoma,nari_posY):
		self.motigoma = motigoma
		self.name = name
		self.nari_posY = nari_posY

	def select(self.ban,screen):
		pass

	def play(self,ban,screen):
		#koma and pfield select
		info = self.select(ban,screen)

		koma = info["koma"]
		pos = info["pos"]
		motigoma_flag = info["motigoma_flag"]
		
		tryFlag = False
		
		if motigoma_select:
			self.motigoma.koma_lst.remove(koma)	
			koma_group.add(koma)
		#nari
		elif isinstance(koma,Fu) and pos[1] == self.nari_posY and koma.nariFlag == False:
			koma.nari()
		#ou try
		elif isinstance(koma,Ou) and pos[1] == self.nari_posY:	
			tryFlag = True

		torigoma = ban.komaMove(koma,pos,self.motigoma,motigoma_flag,self.name)
		koma.posUpdate(pos)

		#f kill king and tryi then win
		if isinstance(torigoma,Ou) or tryFlag:
			return True
		else: return False
	

def collectKoma(owner_name,ban):
		koma_lst = []
		for vlst in ban.field:
			for koma in vlst:
				if koma!=0 and koma.owner == owner_name:
					koma_lst.append(koma)
		return koma_lst

def collectPos(ban,fn):
	pos_lst = []

	for j,vlst in enumerate(ban):
		for i,val in enumerate(vlst):
			if i>=1 and i<=3 and j>=1 and j <=4:
				if fn(val):
					pos_lst.append((i,j))
	return pos_lst

def isRegal(ban,pos,owner_name):
	posX = pos[0]
	posY = pos[1]

	val = ban[posY][posX] 
	if posX>=1 and posX<=3 and posY>=1 and posY<=4:
		if isinstance(val,int):
			if val == 0:
				return True
		elif val.owner != owner_name:
			return True
		else: return False
	#over field
	else: return False
		

def collectMoveablePos(ban,koma,owner_name):
	pos_lst = []
	for dir in koma.dir_lst:
		posX = koma.posX + dir[0]
		posY = koma.posY + dir[1] 

		if isRegal(ban,(posX,posY),owner_name):
			pos_lst.append((posX,posY))

	return pos_lst


class Human(gamePlayer):
	def __init__(self,motigoma):
		gamePlayer.__init__(self,"player",motigoma,1)

	def selectKoma(self,ban,screen):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
		 		if event.type == pygame.MOUSEBUTTONUP:
		 			pos = pygame.mouse.get_pos()
						
					koma_lst = collectKoma("player",ban)
                               	 	 #turn card      
					select_koma = False
                        		for koma in koma_lst:
						if koma.rect.collidepoint(pos):
							select_koma = koma
							pos_lst = collectMoveablePos(ban.field,koma,"player")

					for koma in self.motigoma.koma_lst:
						if koma.rect.collidepoint(pos):
							select_koma = koma
							pos_lst = collectPos(ban.field,lambda val:val == 0)

					ban.brightFiled(screen,pos_lst)
					return select_koma

	def selectField(self,ban,koma,motigoma_flag):
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
			 	if event.type == pygame.MOUSEBUTTONUP:
			 		pos = pygame.mouse.get_pos()
					if pos[0] >= 280 and pos[0] < 520:
						posX = (pos[0]-280)/80+1
						posY = pos[1]/100+1

						if motigoma_flag == False:
							#collect pos that empty or cpu's koma excists
							pos_lst = collectMoveablePos(ban.field,koma,"player")
						else:	
							#collect pos that empty
							pos_lst = collectPos(ban.field,lambda val:val == 0)

						if [] != filter(lambda lst:lst[0] == posX and lst[1] == posY,pos_lst):
								return [posX,posY]
						else:
							return False
	def select(self,ban,screen):
		while 1:
			koma = self.selectKoma(ban,screen)
		
			if self.motigoma.is_excist(koma):
				motigoma_Flag = True
			else:   motigoma_Flag = False

			pos = self.selectField(ban,koma,motigoma_Flag)

			if pos != False:
				
				break
		        else:	
				ban.draw(screen)
				koma_group.draw(screen)
				pygame.display.update()

			return {"koma":koma,"pos":pos,"motigoma_Flag":motigomaFlag}

class Computer(gamePlayer):
	def __init__(self,motigoma):
		gamePlayer.__init__(self,"cpu",motigoma,4)

	def selectFromBan(self,ban):	
		koma_lst = collectKoma("cpu",ban)
		rand_num = random.randint(0,len(koma_lst)-1)

		return koma_lst[rand_num]
	
	def selectFromMotigoma(self):	
		koma_lst = self.motigoma.koma_lst
		rand_num = random.randint(0,len(koma_lst)-1)

		return koma_lst[rand_num]

	def selectKoma(self,ban):
		if self.motigoma.koma_lst == []:
			koma =	self.selectFromBan(ban)
		else:
			rand_num = random.randint(0,1)
			if rand_num == 0:
				koma =	self.selectFromBan(ban)
			else:	koma =	self.selectFromMotigoma()

		return koma

	def selectField(self,ban,koma,motigoma_flag):
		if motigoma_flag == False:
			#collect pos that empty or cpu's koma excists
			pos_lst = collectMoveablePos(ban.field,koma,"cpu")
		else:	
			#collect pos that empty
			pos_lst = collectPos(ban.field,lambda val:val == 0)
		
		if pos_lst == []:
			return False
		else:
			rand_num = random.randint(0,len(pos_lst)-1)
			return pos_lst[rand_num]

	def select(self,ban,screen):
		while 1:
			koma = self.selectKoma(ban)
		
			if self.motigoma.is_excist(koma):
				motigoma_Flag = True
			else:   motigoma_Flag = False

			pos = self.selectField(ban,koma,motigoma_Flag)

			if pos != False:
				
				break
		        
			return {"koma":koma,"pos":pos,"motigoma_Flag":motigomaFlag}

def main():
	pygame.init()
	screen = pygame.display.set_mode(size)
	ban = Ban(280,0)

	motigoma= Motigoma((530,300),(80,-100))
	motigoma2= Motigoma((180,0),(-80,100))

	player = Human(motigoma)
	cpu = Computer(motigoma2)

	screen.fill(black)
	ban.draw(screen)
	koma_group.draw(screen)
	pygame.display.update()

	def drawAll():
		screen.fill(black)
		ban.draw(screen)
		player.motigoma.komaDraw(screen)
		cpu.motigoma.komaDraw(screen)
		koma_group.draw(screen)
		pygame.display.update()
	
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()
                                 #turn card      
				#ban.komaDraw(screen)
		#ban.komaDraw2(screen)
		#play(ban,motigoma)
		player_win = player.play(ban,screen)
		drawAll()
		if player_win:
			print "player win"
			time.sleep(0.5)
			sys.exit()

		time.sleep(0.5)

		cpu_win = cpu.play(ban,screen)
		drawAll()
		if cpu_win:
			print "cpu win"
			time.sleep(0.5)
			sys.exit()

		time.sleep(0.5)

main()

#todo outenige,nige,tori
