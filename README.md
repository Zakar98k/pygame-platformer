
# pygame-platformer
A basic platformer built with a library called PyGame with Python. Inspired by DaFluffyPotato's platformer code

## DOCUMENTATION
### In Platformer.py

#### blit_parallax_bg
TODO finish defining a function where you pass in a list of objects and blits them onto the screen, creating a parallax effect.
What it does: 
- the function takes in a list of rects to blit onto the screen, creating a parallax effect.

```python
def blit_parallax_bg(objects=[]):
    i = 0
    if not objects is []:
        for object in objects: 
            pygame.draw(rect, )
```

#### image_outline
What it does:
- takes in an `img` and its current `loc`, and blits an outline surrounding the img.
- Useful for creating 1px shadow outlines

```python
def image_outline(img,loc,surf=display): 
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface(setcolor=(30,30,30),unsetcolor=(0,0,0))
    mask_surf.set_colorkey((0,0,0))
    surf.blit(mask_surf,(loc[0]+1,loc[1]+1),special_flags=BLEND_RGB_SUB)
    surf.blit(mask_surf,(loc[0]+2,loc[1]+1),special_flags=BLEND_RGB_SUB)
    surf.blit(mask_surf,(loc[0]+1,loc[1]+2),special_flags=BLEND_RGB_SUB)
```

#### load_map
What it does: 
- loads in the game map file, taking in the file's `path`. 
- Returns a list called `game_map`, where each item in the list is a "row", which itself is a a list that contains tiles and tile data. An empty item in `game_map` represents an empty row with no tiles
- the list returned should look like this:
	- `[[], [], [], [], [], [], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '3', '1', '1', '1', '4'], ['0', '0', '0', '0', '3', '1', '1', '1', '1', '1', 'a', '2', '2', '2', 'b', '1', '1', '1', '4'], ['0', '0', '0', '0', '5', 'c', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '8', '0', '0', '0', '0', '0', '3', '1', '1', '1', '4'], ['0', '0', '0', '0', '0', '5', '9', '9', 'c', '2', '2', '2', '2', '2', '2', 'd', '9', '9', '6', '0', '0', '0', '0', '0', '0', '5', '9', '6'], ['0', '0', '0', '0', '0', '0', '0', '0', '5', '9', '9', '9', '9', '9', '9', '6'], [], [], [], ['3', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '4'], ['5', 'c', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', 'd', '6'], ['0', '5', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '6', '0'], [], [], [], [], [], []]`
```python
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
```

### In engine.py
#### collision_test
What it does:
- Returns a list of objects from `object_list` that have collided with `object_1`
- useful for checking for single/multiple collisions with a player or another object
```python
def collision_test(object_1,object_list):
    collision_list = []
    for obj in object_list:
        if obj.colliderect(object_1):
            collision_list.append(obj)
    return collision_list
```

#### class physics_obj
##### Move
What it does:
- Handles the movement and collisions of an object
- `movement[0]`is added to `self.x` in order for movement on the x-axis to occur
- handles collisions by calling the `collision_test` function and storing the objects that collided with `self` in a variable called `block_hit_list`.
	- for each object in block hit list, 

```python
    def move(self,movement,platforms,ramps=[]):
        self.x += movement[0]
        self.rect.x = int(self.x)
        # block_hit_list contains a list of objects that collided with self.rect
        block_hit_list = collision_test(self.rect,platforms)
        collision_types {'top':False,'bottom':False,'right':False,'left':False,'slant_bottom':False,'data':[]}
        # added collision data to "collision_types". ignore the poorly chosen variable name
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[0] > 0:
                self.rect.right = block.left
                collision_types['right'] = True
                markers[0] = True
            elif movement[0] < 0:
                self.rect.left = block.right
                collision_types['left'] = True
                markers[1] = True
            collision_types['data'].append([block,markers])
            self.x = self.rect.x
        self.y += movement[1]
        self.rect.y = int(self.y)
        block_hit_list = collision_test(self.rect,platforms)
        for block in block_hit_list:
            markers = [False,False,False,False]
            if movement[1] > 0:
                self.rect.bottom = block.top
                collision_types['bottom'] = True
                markers[2] = True
            elif movement[1] < 0:
                self.rect.top = block.bottom
                collision_types['top'] = True
                markers[3] = True
            collision_types['data'].append([block,markers])
            self.change_y = 0
            self.y = self.rect.y
        return collision_types
```
