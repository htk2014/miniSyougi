import sys
import  pygame 
import os
import time
import random

import util
import koma as syougi_koma
import ai as syougi_ai

size = width, height = 800, 400
black = 0, 0, 0
class Motigoma(object):
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

class Ban(object):
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
		s_fu = syougi_koma.Fu(fu_front_img_lst,fu_nari_img_lst,fu_dir,fu_nari_dir,(2,3),"s_fu","player")
		g_fu = syougi_koma.Fu(fu_front_img_lst,fu_nari_img_lst,fu_dir,fu_nari_dir,(2,2),"g_fu","cpu")

		kaku_img_lst ={"player":"./img/koma/kakuA.png","cpu":"./img/koma/kakuB.png"}
		kaku_dir = [(-1,-1),(1,1),(-1,1),(1,-1)]
		s_kaku = syougi_koma.Koma(kaku_img_lst,kaku_dir,(1,4),"s_kaku","player")
		g_kaku = syougi_koma.Koma(kaku_img_lst,kaku_dir,(3,1),"g_kaku","cpu")

		hi_img_lst ={"player":"./img/koma/hiA.png","cpu":"./img/koma/hiB.png"}
		hi_dir = [(1,0),(-1,0),(0,1),(0,-1)]
		s_hi = syougi_koma.Koma(hi_img_lst,hi_dir,(3,4),"s_hi","player")
		g_hi = syougi_koma.Koma(hi_img_lst,hi_dir,(1,1),"g_hi","cpu")

		ou_img_lst ={"player":"./img/koma/ouA.png","cpu":"./img/koma/ouB.png"}
		ou_dir = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(1,1),(-1,1),(1,-1)]
		s_ou = syougi_koma.Ou(ou_img_lst,ou_dir,(2,4),"s_ou","player")
		g_ou = syougi_koma.Ou(ou_img_lst,ou_dir,(2,1),"g_ou","cpu")
		
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
		else: torigoma = False

		self.field[newPos[1]][newPos[0]] = koma

		return torigoma

	def komaDraw(self,screen):
		for vlst in self.field:
			for koma in vlst:
				if not(util.isZero(koma)):
					screen.blit(koma.image,koma.rect)

class gamePlayer(object):
	def __init__(self,name,motigoma,nari_posY):
		self.motigoma = motigoma
		self.name = name
		self.nari_posY = nari_posY

	def select(self,ban,screen):
		pass

	def play(self,ban,screen):
		#koma and pfield select
		info = self.select(ban,screen)

		koma = info["koma"]
		pos = info["pos"]
		motigoma_flag = info["motigoma_flag"]
		
		tryFlag = False
		
		if motigoma_flag:
			self.motigoma.koma_lst.remove(koma)	
		#nari
		elif isinstance(koma,syougi_koma.Fu) and pos[1] == self.nari_posY and koma.nariFlag == False:
			koma.nari()
		#ou try
		elif isinstance(koma,syougi_koma.Ou) and pos[1] == self.nari_posY:	
			tryFlag = True

		torigoma = ban.komaMove(koma,pos,self.motigoma,motigoma_flag,self.name)
		koma.posUpdate(pos)

		#f kill king and tryi then win
		if isinstance(torigoma,syougi_koma.Ou) or tryFlag:
			return True
		else: return False
	
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
						
					koma_lst = util.collectKoma(ban,"player")
                               	 	 #turn card      
					select_koma = False
					pos_lst = False
                        		for koma in koma_lst:
						if koma.rect.collidepoint(pos):
							select_koma = koma
							pos_lst = util.collectMoveablePos(ban,koma,"player")

					for koma in self.motigoma.koma_lst:
						if koma.rect.collidepoint(pos):
							select_koma = koma
							pos_lst = util.collectPos(ban,lambda val:val == 0)

					if pos_lst !=False:
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
							pos_lst = util.collectMoveablePos(ban,koma,"player")
						else:	
							#collect pos that empty
							pos_lst = util.collectPos(ban,lambda val:val == 0)

						if [] != filter(lambda lst:lst[0] == posX and lst[1] == posY,pos_lst):
								return [posX,posY]
						else:
							return False
	def select(self,ban,screen):
		while 1:
			koma = self.selectKoma(ban,screen)
		
			if self.motigoma.is_excist(koma):
				motigoma_flag = True
			else:   motigoma_flag = False

			pos = self.selectField(ban,koma,motigoma_flag)

			if pos != False:
				
				break
		        else:	
				ban.draw(screen)
				ban.komaDraw(screen)
				pygame.display.update()

		return {"koma":koma,"pos":pos,"motigoma_flag":motigoma_flag}

class Computer(gamePlayer):
	def __init__(self,motigoma):
		gamePlayer.__init__(self,"cpu",motigoma,4)
		self.ai =syougi_ai.AI(self)

	def select(self,ban,screen):
		return self.ai.think(ban)
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
	ban.komaDraw(screen)
	pygame.display.update()
	time.sleep(0.5)

	first_player_num = random.randint(0,1)
	if first_player_num ==0:
		first_player = player
		second_player = cpu
	else:
		first_player = cpu
		second_player = player

	def drawAll():
		screen.fill(black)
		ban.draw(screen)
		player.motigoma.komaDraw(screen)
		cpu.motigoma.komaDraw(screen)
		ban.komaDraw(screen)
		pygame.display.update()

	def gameEnd(game_player,win_flag):
		name = game_player.name
		if win_flag:
			print name,"win"
			time.sleep(0.5)
			sys.exit()
	def play(game_player):
		win_flag = game_player.play(ban,screen)
		drawAll()
		gameEnd(game_player,win_flag)

		time.sleep(0.5)
			
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		 	if event.type == pygame.MOUSEBUTTONUP:
		 		pos = pygame.mouse.get_pos()

			play(first_player)
			play(second_player)

if __name__=='__main__':
	main()

