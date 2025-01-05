import numpy as np
import cv2
import heapq

# Uncomment below for manual use
# START_TILE = (40, 21)
# END_TILE = (0, 19)

def count_min_pixel(img,pixel,row_column_exchange = False):
    state = 0
    count = 0
    min_count = img.shape[0]
    for j in range(img.shape[0]):
        state = 0
        count = 0
        for i in range(img.shape[1]):

            if row_column_exchange == False:
                row = i
                column = j
            else:
                row = j
                column = i

            if img[column,row]==(255-pixel) and (state == 0 or state ==1):
                state = 1
            elif img[column,row]==pixel and (state == 1 or state==2):
                count+=1
                state=2
            elif img[column,row]==(255-pixel) and state == 2:
                if count < min_count:
                    min_count = count
                else:
                    count = 0
                    state = 1

    return min_count

def convert_map(img,thresh_black,thresh_white):
    j = 0
    i = 0
    state = 0
    line=[]
    new_img=[]
    while(j<img.shape[0]):
        line=[]
        i=0
        state = 0 
        while(i<img.shape[1]):
            if state == 0:
                line.append(np.average(img[j,i:i+thresh_black]))
                i += thresh_black
                state = 1
            else:
                line.append(np.average(img[j,i:i+thresh_white]))
                i += thresh_white
                state = 0
        new_img.append(line)
        j+=1

    j = 0
    i = 0
    state = 0
    line=[]
    img=np.array(new_img)
    new_img=[]
    while(i<img.shape[1]):
        line=[]
        j=0
        state = 0 
        while(j<img.shape[0]):
            if state == 0:
                line.append(np.mean(img[j:j+thresh_black,i]))
                j += thresh_black
                state = 1
            else:
                line.append(np.mean(img[j:j+thresh_white,i]))
                j += thresh_white
                state = 0
        new_img.append(line)
        i+=1
    
    return np.transpose(np.array(new_img,np.uint8))

def find_start_end(map):
    points = []
    for i,tile in enumerate(map[0,:]):
        if tile == 255:
            points.append((0,i))
    for i,tile in enumerate(map[-1,:]):
        if tile == 255:
            points.append((map.shape[0]-1,i))
    for i,tile in enumerate(map[:,0]):
        if tile == 255:
            points.append((i,0))
    for i,tile in enumerate(map[:,-1]):
        if tile == 255:
            points.append((i,map.shape[1]-1))
    
    return points
    
def heuristic(row, col):
    return abs(END_TILE[0] - row) + abs(END_TILE[1] - col)

def neighbors(row, col,map):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    result = []
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < map.shape[0] and 0 <= c < map.shape[1] and map[r,c] != 0:
            result.append((r, c))
    return result

def a_star(map):
    open_set = []
    heapq.heappush(open_set, (0, START_TILE))
    came_from = {}
    g_score = {START_TILE: 0}
    f_score = {START_TILE: heuristic(*START_TILE)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == END_TILE:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in neighbors(*current,map):
            tentative_g = g_score.get(current, float('inf')) + 1
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(*neighbor)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

def maze_with_path(map,maze,path,ratio):
    map_rgb = np.dstack((map,map,map))
    maze_rgb = np.dstack((maze,maze,maze))
    ratio = ratio//2 
    print(maze.shape[0],map.shape[0])
    map_rgb[START_TILE] = (0,255,0)
    prev = (START_TILE[1]*ratio, START_TILE[0]*ratio)
    for r, c in path:
        map_rgb[r,c] = (0,255,0)
        cv2.line(maze_rgb,prev,(c*ratio,r*ratio),(0,255,0),5)
        prev = (c*ratio,r*ratio)
    cv2.imshow("solved",map_rgb)
    cv2.imshow("realpic",maze_rgb)
    cv2.waitKey(0)
    
maze = cv2.imread("maze.png")
maze = cv2.cvtColor(maze,cv2.COLOR_BGR2GRAY)
_,maze = cv2.threshold(maze,80,255,cv2.THRESH_BINARY)
maze = maze[3:-1,2:-2]
min_count_white = min(count_min_pixel(maze,255),count_min_pixel(maze,255,True))
min_count_black = min(count_min_pixel(maze,0),count_min_pixel(maze,0,True))
map = convert_map(maze,min_count_black,min_count_white)
# Comment below for manual use
START_TILE,END_TILE = find_start_end(map)
path = a_star(map)
if path:
    maze_with_path(map,maze,path,min_count_white+min_count_black)
else:
    print("No path found.")


