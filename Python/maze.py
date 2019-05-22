#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 12:34:23 2018

@author: yuta
"""


import sys
from copy import deepcopy
from collections import defaultdict
import os

class MazeError(Exception):
    def __init__(self,message):
        self.message = message

class Maze:
    def __init__(self,file_name):
        try:
            with open(file_name,'r') as f:
                data = [v.split() for v in f.readlines() if v != '\n']
                #print(file_name)
            #print(data)
            if len(data[0]) == 1:
                j = 0
                for i in data:
                    data[j] = [int(j) for j in i[0]]
                    j += 1
            else:
                data = [list(map(int,v)) for v in data if v != []]
            
            #print(data)
            #print(len(data))
            if len(data) < 2 or len(data) > 41:
                raise MazeError('Incorrect input.')
            keep_row = len(data[0])
            for row in data:
                if len(row) < 2 or len(row) > 31:
                    raise MazeError('Incorrect input.')
                if len(row) != keep_row:
                    raise MazeError('Incorrect input.')
                
            for i in data:
                for j in i:
                    if j != 0 and j != 1 and j != 2 and j != 3:
                        raise MazeError('Incorrect input.')
            for i in data:
                if i[-1] != 0 and i[-1] != 2:
                    raise MazeError('Input does not represent a maze.')
            if 2 in data[-1] or 3 in data[-1]:
                raise MazeError('Input does not represent a maze.')
                
        except FileNotFoundError:
            print('Sorry, there is no such file.')
            sys.exit()
        #print(file_name)
        self.maze_list = data
        self.m_list = deepcopy(data)
        self.p_list = deepcopy(data)
        #self.a_p_list = deepcopy(data)
        self.height = len(data)
        self.width = len(data[0])
        self.sacs = defaultdict(int)
        self.sac_list = []
        self.unique_paths = []
        self.file_name = file_name[:-3] + 'tex'
        self.path_lists = []
    def number_gates(self):
        h_line_top = self.maze_list[0][:-1]
        h_line_below = self.maze_list[-1][:-1]
        gate_lists = []
        
        for x in range(self.width - 1):
            if h_line_top[x] == 0 or h_line_top[x] == 2:
                gate_lists.append((x,0))
            if h_line_below[x] == 0:
                gate_lists.append((x,self.height - 2))
                
        v_line_left = [i[0] for i in self.maze_list][:-1]
        v_line_right = [i[-1] for i in self.maze_list][:-1]
        
        for y in range(self.height - 1):
            if v_line_left[y] == 0 or v_line_left[y] == 1:
                gate_lists.append((0,y))
            if v_line_right[y] == 0:
                gate_lists.append((self.width - 2,y))
        
        return gate_lists
    
    def _connect_right(self,x,y,m_list):
        value = m_list[y][x]
        if value is 1 or value is 3:
            return True
        else:
            return False
        
    def _connect_left(self,x,y,m_list):
        if not (0 <= x - 1 < self.width and 0 <= y < self.height):
            return False
        
        value = m_list[y][x - 1]
        if value is 1 or value is 3:
            return True
        else:
            return False
        
    def _connect_above(self,x,y,m_list):
        if not (0 <= x < self.width and 0 <= y - 1 < self.height):
            return False
        
        value = m_list[y - 1][x]
        if value is 2 or value is 3:
            return True
        else:
            return False
           
    def _connect_below(self,x,y,m_list):
        value = m_list[y][x]
        if value is 2 or value is 3:
            return True
        else:
            return False
        
        
    def explore_wall(self):
        wall_lists = []
        for y in range(self.height):
            for x in range(self.width):
                value = self.m_list[y][x]
                if value is not 0 and value is not -1: 
                    pt_1 = (x,y)
                    wall_list = []
                    wall = self._explore_wall(pt_1,wall_list)
                    wall_lists.append(wall)
                else:
                    pass
        return wall_lists
    
    def _explore_wall(self,pt_1,wall_list):
        
        x,y = pt_1
        #print(x,y)
        
        if not (0 <= x < self.width and 0 <= y < self.height):
            return 
        #もっと上手くかける
        if pt_1 in wall_list:
            return
        
        wall_list.append(pt_1)
        #print(wall_list)
        pt_right,pt_left,pt_above,pt_below = None,None,None,None
        #self.m_list[y][x] = -1
        
        if self._connect_right(x,y,self.m_list):
            pt_right = (x + 1,y)
        
        if self._connect_left(x,y,self.m_list):
            pt_left = (x - 1,y)
        
        if self._connect_above(x,y,self.m_list):
            pt_above = (x,y - 1)
        
        if self._connect_below(x,y,self.m_list):
            pt_below = (x,y + 1)
        
        self.m_list[y][x] = -1
        
        if pt_right is not None:
            self._explore_wall(pt_right,wall_list)
        if pt_left is not None:
            self._explore_wall(pt_left,wall_list)
        if pt_above is not None:
            self._explore_wall(pt_above,wall_list)
        if pt_below is not None:
            self._explore_wall(pt_below,wall_list)
        
        return wall_list
    
    
    def path_right(self,x,y,p_list):
        #if not (0 <= x + 1 < self.width and 0 <= y < self.height):
            #return False
        value = p_list[y][x + 1]
        if value is 1 or value is 0:
            return True
        else:
            return False
        
    def path_left(self,x,y,p_list):
        #if not (0 <= x - 1 < self.width and 0 <= y < self.height):
            #return False
        
        value = p_list[y][x]
        if value is 1 or value is 0:
            return True
        else:
            return False
        
    def path_above(self,x,y,p_list):
        #if not (0 <= x < self.width and 0 <= y - 1 < self.height):
            #return False
        
        value = p_list[y][x]
        if value is 0 or value is 2:
            return True
        else:
            return False
           
    def path_below(self,x,y,p_list):
        #if not (0 <= x < self.width and 0 <= y + 1 < self.height):
            #return False
        
        value = p_list[y + 1][x]
        if value is 0 or value is 2:
            return True
        else:
            return False
   
    def explore_path(self,gate_lists):
        path_lists = []
        for pt_1 in gate_lists:
            x,y = pt_1
            value = self.p_list[y][x]
            if value is not -1:
                path_list = []
                path = self._explore_path(pt_1,path_list)
                path_lists.append(path)
            else:
                pass
        return path_lists
    
    def _explore_path(self,pt_1,path_list):
        
        x,y = pt_1

        if not (0 <= x < self.width -1 and 0 <= y < self.height - 1):
            return 
        if pt_1 in path_list:
            return
        
        path_list.append(pt_1)
        pt_right,pt_left,pt_above,pt_below = None,None,None,None
        
        if self.path_right(x,y,self.p_list):
            #self.sacs[(x,y)] = self.sacs[(x,y)] + 1
            pt_right = (x + 1,y)       
        if self.path_left(x,y,self.p_list):
            #self.sacs[(x,y)] = self.sacs[(x,y)] + 1
            pt_left = (x - 1,y) 
        if self.path_above(x,y,self.p_list):
            #self.sacs[(x,y)] = self.sacs[(x,y)] + 1
            pt_above = (x,y - 1)
        if self.path_below(x,y,self.p_list):
            #self.sacs[(x,y)] = self.sacs[(x,y)] + 1
            pt_below = (x,y + 1)
            
        self.p_list[y][x] = -1
        
        if pt_right is not None:
            self._explore_path(pt_right,path_list)
        if pt_left is not None:
            self._explore_path(pt_left,path_list)
        if pt_above is not None:
            self._explore_path(pt_above,path_list)
        if pt_below is not None:
            self._explore_path(pt_below,path_list)
        
        return path_list
    
    def cul_de_sacs(self,path_lists):
        for i in path_lists:
            for pt_1 in i:
                x,y = pt_1
                if self.path_right(x,y,self.maze_list):
                    self.sacs[(x,y)] = self.sacs[(x,y)] + 1
                if self.path_left(x,y,self.maze_list):
                    self.sacs[(x,y)] = self.sacs[(x,y)] + 1
                if self.path_above(x,y,self.maze_list):
                    self.sacs[(x,y)] = self.sacs[(x,y)] + 1
                if self.path_below(x,y,self.maze_list):
                    self.sacs[(x,y)] = self.sacs[(x,y)] + 1
                    
        return self.sacs
    
                        
    def connect_check(self,pt_1,sac_list):
        x,y = pt_1
        left_0 = (x-1,y)
        right_0 = (x+1,y)
        above_0 = (x,y-1)
        below_0 = (x,y+1)
        
        if left_0 in sac_list:
            return True
        if right_0 in sac_list:
            return True
        if above_0 in sac_list:
            return True
        if below_0 in sac_list:
            return True
        
        return False

    def count_sacs(self,path_lists):
#        cnt = 0
        for path_list in path_lists:
#            cnt += 1
            if 1 in [self.sacs[pt_1] for pt_1 in path_list]:
                self._count_sacs(path_list)
#        return cnt       
        sac_lists = []
        for path_list in path_lists:
            sac_list = []
            for pt_1 in path_list:
                if self.sacs[pt_1] == 0:
                    #print(pt_1)
                    if sac_list == []:
                        sac_list.append(pt_1)
                    else:
                        if self.connect_check(pt_1,sac_list):
                            sac_list.append(pt_1)
                        else:
                            sac_lists.append(sac_list)
                            sac_list = []
                            sac_list.append(pt_1)
                else:
                    if sac_list != []:
                        sac_lists.append(sac_list)
                        sac_list = []
            if sac_list != []:
                sac_lists.append(sac_list)
        #print(sac_lists)
        for i in sac_lists:
            for j in i:
                self.sac_list.append(j)
        return sac_lists
                    
    def _count_sacs(self,path_list):
        #count_sac = 0
        for pt_1 in path_list:
            if self.sacs[pt_1] == 1:
                #self.count_sac += 1
                self.sacs[pt_1] -= 1
                x,y = pt_1
                left_1 = (x-1,y)
                    #make_list_for_sacs
                if left_1 in path_list and self.sacs[left_1] != 0:
                    if self.path_left(x,y,self.maze_list):
                #if left_1 in path_list and self.path_left(x-1,y,self.maze_list) and self.sacs[left_1] != 0 :
                        self.sacs[left_1] = self.sacs[left_1] - 1
                        return self._count_sacs(path_list)
                right_1 = (x+1,y)

                if right_1 in path_list and self.sacs[right_1] != 0:
                #if right_1 in path_list and self.path_right(x+1,y,self.maze_list) and self.sacs[right_1] != 0:
                    if self.path_right(x,y,self.maze_list):
                        self.sacs[right_1] = self.sacs[right_1] - 1
                        return self._count_sacs(path_list)
                above_1 = (x,y-1)
                if above_1 in path_list and self.sacs[above_1] != 0:
                #if above_1 in path_list and self.path_above(x,y-1,self.maze_list) and self.sacs[above_1] != 0:
                    if self.path_above(x,y,self.maze_list):
                        self.sacs[above_1] = self.sacs[above_1] - 1
                        return self._count_sacs(path_list)
                below_1 = (x,y+1)
                if below_1 in path_list and self.sacs[below_1] != 0:
                #if below_1 in path_list and self.path_below(x,y+1,self.maze_list) and self.sacs[below_1] != 0:
                    if self.path_below(x,y,self.maze_list):
                        self.sacs[below_1] = self.sacs[below_1] - 1
                        return self._count_sacs(path_list)

    def final_path(self,path_lists):
        unique_paths = []
        for path_list in path_lists:
            check_path = [self.sacs[pt_1] for pt_1 in path_list]
            if 3 in check_path or 4 in check_path:
                pass
            elif any(check_path):
                unique_path = [pt_1 for pt_1 in path_list if self.sacs[pt_1] == 1 or self.sacs[pt_1] == 2]
                unique_paths.append(unique_path)
            else:
                pass
        self.unique_paths = unique_paths
        #print(unique_paths)
        return unique_paths
                
    def p_right(self,x,y,p_list):
        #if not (0 <= x + 1 < self.width and 0 <= y < self.height):
            #return False
        value = p_list[y][x]
        if value is 0 or value is 2:
            return True
        else:
            return False
        
    def p_left(self,x,y,p_list):
        if not (0 <= x - 1 < self.width and 0 <= y < self.height):
            return True
        
        value = p_list[y][x - 1]
        if value is 0 or value is 2:
            return True
        else:
            return False
        
    def p_above(self,x,y,p_list):
        if not (0 <= x < self.width and 0 <= y - 1 < self.height):
            return True
        
        value = p_list[y - 1][x]
        if value is 0 or value is 1:
            return True
        else:
            return False
           
    def p_below(self,x,y,p_list):
        #if not (0 <= x < self.width and 0 <= y + 1 < self.height):
            #return False
        
        value = p_list[y][x]
        if value is 0 or value is 1:
            return True
        else:
            return False

    def f_right(self,x,y,p_list):
        if not (0 <= x + 1 < self.width and 0 <= y < self.height):
            return True
        value = p_list[y][x + 1]
        if value is 0 or value is 1:
            return True
        else:
            return False
        
    def f_left(self,x,y,p_list):
        #if not (0 <= x - 1 < self.width and 0 <= y < self.height):
            #return True
        
        value = p_list[y][x]
        if value is 0 or value is 1:
            return True
        else:
            return False
        
    def f_above(self,x,y,p_list):
        #if not (0 <= x < self.width and 0 <= y - 1 < self.height):
            #return True
        
        value = p_list[y][x]
        if value is 0 or value is 2:
            return True
        else:
            return False
           
    def f_below(self,x,y,p_list):
        if not (0 <= x < self.width and 0 <= y + 1 < self.height):
            return True
        
        value = p_list[y + 1][x]
        if value is 0 or value is 2:
            return True
        else:
            return False

#    def connect_unique_path(self,x,y,ee_path):
#        from_x = x + 0.5
#        from_y = y + 0.5
#        if self.f_above(x,y,self.maze_list) and (x,y - 1) not in ee_path:
#            #save
#            from_y = from_y - 1
#            #print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
#        if self.f_below(x,y,self.maze_list):
#            #to_x = from_x
#            #to_y = from_y + 1
#            return self.connect_unique_path(x,y + 1,ee_path)
#            #print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
#        else:
#            to_x = x
#            to_y = from_y + 1
               
        
    def analyse(self):
        
        gate_lists = self.number_gates()
        gate = len(gate_lists)
        if gate == 0:
            print(f'The maze has no gate.')
        elif gate == 1:
            print(f'The maze has a single gate.')
        else:
            print(f'The maze has {gate} gates.')
        
        #print(self.explore_wall())
        wall_lists = self.explore_wall()
        #print(wall_lists)
        wall = len(wall_lists)
        if wall == 0:
            print(f'The maze has no wall.')
        elif wall == 1:
            print(f'The maze has walls that are all connected.')
        else:
            print(f'The maze has {wall} sets of walls that are all connected.')
            
        path_lists = self.explore_path(gate_lists)
        self.path_lists = path_lists
        #print(path_lists)
        total_block = (self.height - 1) * (self.width - 1)       
        accessible_block = 0
        for i in path_lists:
            accessible_block = accessible_block + len(i)
            
        inaccessible_block = total_block - accessible_block
        if inaccessible_block == 0:
            print(f'The maze has no inaccessible inner point.')
        elif inaccessible_block == 1:
            print(f'The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {inaccessible_block} inaccessible inner points.')

        #print(inaccessible_block)
        path = len(path_lists)
        if path == 0:
            print(f'The maze has no accessible area.')
        elif path == 1:
            print(f'The maze has a unique accessible area.')
        else:
            print(f'The maze has {path} accessible areas.')
            
        #print(self.cul_de_sacs(path_lists))
        self.cul_de_sacs(path_lists)
        
        sacs = len(self.count_sacs(path_lists))
        if sacs == 0:
            print(f'The maze has no cul-de-sac.')
        elif sacs == 1:
            print(f'The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {sacs} sets of accessible cul-de-sacs that are all connected.')
            
        unique_path = len(self.final_path(path_lists))
        if unique_path == 0:
            print(f'The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif unique_path == 1:
            print(f'The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {unique_path} entry-exit paths with no intersections not to cul-de-sacs.')

    def display(self):
        tex_filename = self.file_name
        gate_lists = self.number_gates()
        wall_lists = self.explore_wall()
        #print(wall_lists)
        path_lists = self.explore_path(gate_lists)
        #print(path_lists)
        self.cul_de_sacs(path_lists)
        sacs = len(self.count_sacs(path_lists))
        #unique_path = len(self.final_path(path_lists))
        unique_path = self.final_path(path_lists)
        #print(unique_path)
        e_e_path = [j for i in unique_path for j in i]
        print(e_e_path)
        #gate_lists = self.number_gates()
        with open(tex_filename, 'w') as tex_file:
            print('\\documentclass[10pt]{article}\n'
                  '\\usepackage{tikz}\n'
                  '\\usetikzlibrary{shapes.misc}\n'
                  '\\usepackage[margin=0cm]{geometry}\n'
                  '\\pagestyle{empty}\n'
                  '\\tikzstyle{every node}=[cross out, draw, red]\n'
                  '\n'
                  '\\begin{document}\n'
                  '\n'
                  '\\vspace*{\\fill}\n'
                  '\\begin{center}\n'
                  '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]', file = tex_file
                  )
            print(f'% Walls', file = tex_file)
            for y in range(self.height):
                connect_x = False
                for x in range(self.width):
                    if self._connect_right(x,y,self.maze_list):
                        if connect_x == False:
                            from_x = x
                            connect_x = True
                        else:
                            pass
                            
                    else:
                        if connect_x == True:
                            to_x = x
                            print(f'    \\draw ({from_x},{y}) -- ({to_x},{y});', file = tex_file)
                            connect_x = False
                        else:
                            pass                  
            for x in range(self.width):
                connect_y = False
                for y in range(self.height):
                    if self._connect_below(x,y,self.maze_list):
                        if connect_y == False:
                            from_y = y
                            connect_y = True
                        else:
                            pass
                    else:
                        if connect_y == True:
                            to_y = y
                            print(f'    \\draw ({x},{from_y}) -- ({x},{to_y});', file = tex_file)
                            connect_y = False
                        else:
                            pass          
            print(f'% Pillars', file = tex_file)
            for y in range(self.height):
                for x in range(self.width):
                    if self.p_left(x,y,self.maze_list) and self.p_right(x,y,self.maze_list) \
                    and self.p_above(x,y,self.maze_list) and self.p_below(x,y,self.maze_list):
                        print(f'    \\fill[green] ({x},{y}) circle(0.2);', file = tex_file)
            
            print(f'% Inner points in accessible cul-de-sacs', file = tex_file)
            #self.cul_de_sacs(self.path_lists)
            sac_list = sorted(self.sac_list,key = lambda k:(k[1],k[0]))
            for pt_1 in sac_list:
                x,y = pt_1
                x = x + 0.5
                y = y + 0.5
                print(f'    \\node at ({x},{y}) ''{};', file = tex_file)
            print(f'% Entry-exit paths without intersections', file = tex_file)
            ee_paths = self.unique_paths
            #print(ee_paths)
            for ee_path in ee_paths:
                connecting = False
                ee_path = sorted(ee_path,key = lambda k:(k[1],k[0]))
                for pt in ee_path:
                    x,y = pt
                    x_point = x + 0.5
                    y_point = y + 0.5
                    if self.f_left(x,y,self.maze_list) and not (0 <= x - 1 < self.width and 0 <= y < self.height):
                        #to_x = from_x
                        from_x = x_point - 1
                        from_y = y_point
                        connecting = True
                        #to_y = from_y
                        #print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
                    if self.f_right(x,y,self.maze_list):
                        if connecting == False:
                            from_x = x_point
                            from_y = y_point
                            connecting = True
                        if not 0 <= x_point + 1 < self.width:
                            to_x = x_point + 1
                            to_y = y_point
                            print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
                    elif connecting == True:
                        if not (0 <= x + 1 < self.width and 0 <= y < self.height):
                            to_x = x_point + 1
                            to_y = y_point
                        else:
                            to_x = x_point
                            to_y = y_point
                        #print(from_x,connecting)
                        print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
                        #print(f'({from_x},{from_y})--({to_x},{to_y})')
                        connecting = False
            #print(ee_paths)
            #print(f'    \draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
            for ee_path in ee_paths:
                connecting = False
                ee_path = sorted(ee_path,key = lambda k:(k[0],k[1]))
                for pt in ee_path:
                    x,y = pt
                    x_point = x + 0.5
                    y_point = y + 0.5
                    if self.f_above(x,y,self.maze_list) and not (0 <= x < self.width and 0 <= y - 1 < self.height):
                        #to_x = from_x
                        from_x = x_point 
                        from_y = y_point - 1
                        connecting = True
                        #to_y = from_y
                        #print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
                    if self.f_below(x,y,self.maze_list):
                        if connecting == False:
                            from_x = x_point
                            from_y = y_point
                            connecting = True
                    elif connecting == True:
                        if not (0 <= x < self.width and 0 <= y + 1 < self.height):
                            to_x = x_point
                            to_y = y_point + 1
                        else:
                            to_x = x_point
                            to_y = y_point
                            #print(from_x,connecting)
                        print(f'    \\draw[dashed, yellow] ({from_x},{from_y}) -- ({to_x},{to_y});', file = tex_file)
                        #print(f'({from_x},{from_y})--({to_x},{to_y})')
                        connecting = False
                            

            print('\\end{tikzpicture}\n'
                  '\\end{center}\n'
                  '\\vspace*{\\fill}\n\n'
                  '\\end{document}', file = tex_file
                  )
        #os.system('pdflatex ' + tex_filename)
