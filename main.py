from tkinter.messagebox import showinfo as msg
from pygame.locals import *
import tkinter as tk
import pygame
import random
import time
win = tk.Tk()
win.withdraw()
pygame.init()
def render(surf,blocks):
	for x,y in blocks.keys():
		renderingf = (x * 40,y * 40)
		color = blocks[(x,y)]
		pygame.draw.rect(surf,color,Rect(renderingf,(40,40)))
class tetris_block:
	def __init__(self):
		self.block = {}
		self.pos = (0,0)
		self.disable = False
	def rand_block(self,s,w,h):
		O = {(0, 0): (0, 255, 0), (0, 1): (0, 255, 0), (1, 0): (0, 255, 0), (1, 1): (0, 255, 0)}
		I = {(0, 0): (0, 0, 255), (1, 0): (0, 0, 255), (2, 0): (0, 0, 255), (3, 0): (0, 0, 255)}
		S = {(0, 1): (255, 0, 0), (0, 2): (255, 0, 0), (1, 0): (255, 0, 0), (1, 1): (255, 0, 0)}
		Z = {(0, 0): (255, 0, 255), (0, 1): (255, 0, 255), (1, 1): (255, 0, 255), (1, 2): (255, 0, 255)}
		L = {(0, 0): (255, 255, 255), (0, 1): (255, 255, 255), (0, 2): (255, 255, 255), (1, 0): (255, 255, 255)}
		J = {(0, 0): (255, 255, 0), (0, 1): (255, 255, 0), (0, 2): (255, 255, 0), (1, 2): (255, 255, 0)}
		T = {(0, 0): (0, 255, 255), (0, 1): (0, 255, 255), (0, 2): (0, 255, 255), (1, 1): (0, 255, 255)}
		self.block = random.choice([O,I,S,Z,L,J,T])
		ma = w - 1 - max(map(lambda it:it[1],list(self.block.keys())))
		if(ma < 0):
			ma = 0
		self.move(random.randint(0,ma),0,w,h)
	def get_block(self):
		res = {}
		for x,y in self.block.keys():
			res[(x + self.pos[0],y + self.pos[1])] = self.block[(x,y)]
		return res
	def rotate(self,W,H):
		if(self.disable):return
		size = [max(map(lambda it:it[0],list(self.block.keys()))),
			max(map(lambda it:it[1],list(self.block.keys())))]
		rotMat = [[0 for j in range(size[0] + 1)] for i in range(size[1] + 1)]
		c = self.block[list(self.block.keys())[0]]
		for i in self.block.keys():
			rotMat[i[1]][i[0]] = 1
		rotMat = rotMat[::-1]
		h,w = len(rotMat),len(rotMat[0])
		mx,my = w + self.pos[0],h + self.pos[1]
		if(mx >= W or my >= H or mx < 0 or my < 0):
			return
		self.block = {}
		for i in range(len(rotMat)):
			for j in range(len(rotMat[i])):
				if(rotMat[i][j]):
					self.block[(i,j)] = c
	def intersect(self,rhs):
		b1 = self.get_block()
		b2 = rhs.get_block()
		if(set(b1) & set(b2)):
			return True
		else:
			return False
	def any_intersect(self,ls):
		for i in ls:
			if(self.intersect(i)):
				return True
		return False
	def landed(self,s):
		if(self.disable):return True
		p = self.pos[1] + max(map(lambda it:it[1],list(self.block.keys()))) + 1
		return p > s
	def flying(self):
		if(self.disable):return False
		return self.pos[1] <= 0
	def move(self,x,y,w,h):
		if(self.disable):return
		if(self.pos[0] + x + max(map(lambda it:it[0],list(self.block.keys()))) + 1 > w or self.pos[0] + x < 0):
			return
		self.pos = (self.pos[0] + x,
			    self.pos[1] + y)
	def removeline(self,l):
		if(self.disable):return
		new = dict(self.block)
		for x,y in self.block:
			if(y + self.pos[1] == l):
				new.pop((x,y))
		proc = lambda it:(it[0],it[0]) if(it[0][1] > l) else (it[0],(it[0][0],it[0][1] + 1))
		upd = dict(dict(map(proc,new.items())))
		res = {}
		for i in upd:
			v = new[i]
			res[upd[i]] = v
		self.block = dict(res)
		if(not new):
			self.disable = True
def main(size):
	scr = pygame.display.set_mode((40 * size[0],40 * size[1]))
	blk_list = []
	n = 1
	speed = 15
	s = 0
	stop = False
	while(1):
		if(not stop):
			d = {}
			for i in blk_list:
				d.update(i.get_block())
			for i in range(size[1]):
				flag = True
				for j in range(size[0]):
					if((j,i) not in d):
						flag = False
				if(flag):
					s += 5
					for j in blk_list:
						j.removeline(i)
		for i in blk_list[:-1]:
			if(i.flying()):
				return s
		pygame.display.update()
		scr.fill((0,0,0))
		n += 1
		n %= speed
		if((not n) and (not stop)):
			if((not blk_list) or blk_list[-1].landed(size[1]) or blk_list[-1].any_intersect(blk_list[:-1])):
				if(blk_list):
					blk_list[-1].move(0,-1,*size)
				b = tetris_block()
				b.rand_block(size[0],*size)
				blk_list.append(b)
			else:
				blk_list[-1].move(0,1,*size)
		for ev in pygame.event.get():
			if(ev.type == QUIT):
				exit()
			elif(ev.type == KEYDOWN and ev.key == K_LEFT and blk_list):
				blk_list[-1].move(-1,0,*size)
				if(blk_list[-1].any_intersect(blk_list[:-1])):
					blk_list[-1].move(1,0,*size)
			elif(ev.type == KEYDOWN and ev.key == K_RIGHT and blk_list):
				blk_list[-1].move(1,0,*size)
				if(blk_list[-1].any_intersect(blk_list[:-1])):
					blk_list[-1].move(-1,0,*size)
			elif(ev.type == MOUSEBUTTONDOWN):
				stop = not stop
			elif(ev.type == KEYDOWN and ev.key in [K_LSHIFT,K_RSHIFT] and blk_list):
				blk_list[-1].rotate(*size)
			elif(ev.type == KEYDOWN and ev.key == K_ESCAPE and stop):
				return s
			elif(ev.type == KEYDOWN and ev.unicode == ' ' and blk_list and (not stop)):
				while(not (blk_list[-1].landed(size[1]) or blk_list[-1].any_intersect(blk_list[:-1]))):
					blk_list[-1].move(0,1,*size)
				blk_list[-1].move(0,-1,*size)
				b = tetris_block()
				b.rand_block(size[0],*size)
				blk_list.append(b)
		if(stop):
			img = pygame.image.load('pause.jpg')
			img = pygame.transform.scale(img,(40 * size[0],40 * size[1]))
			scr.blit(img,(0,0))
		else:
			for blk in blk_list:
				render(scr,blk.get_block())
if(__name__ == '__main__'):
	size = [15,15]
	while(1):
		s = main(size)
		msg('GAMEOVER!','GAMEOVER!  score:%s'%s)
