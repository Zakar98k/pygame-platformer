# pygame-platformer
A basic platformer built with a library called PyGame with Python. Inspired by DaFluffyPotato's platformer code

## DOCUMENTATION
### Functions
#### In Platformer.py

##### blit_parallax_bg
TODO finish defining a function where you pass in a list of objects and blits them onto the screen, creating a parallax effect.
What it does: the function takes in a list of rects to blit onto the screen, creating a parallax effect.

```python
def blit_parallax_bg(objects=[]):
    i = 0
    if not objects is []:
        for object in objects: 
            pygame.draw(rect, )
```

##### image_outline
What it does:
- takes in an 

```python
def image_outline(img,loc,surf=display): 
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface(setcolor=(30,30,30),unsetcolor=(0,0,0))
    mask_surf.set_colorkey((0,0,0))
    surf.blit(mask_surf,(loc[0]+1,loc[1]+1),special_flags=BLEND_RGB_SUB)
    surf.blit(mask_surf,(loc[0]+2,loc[1]+1),special_flags=BLEND_RGB_SUB)
    surf.blit(mask_surf,(loc[0]+1,loc[1]+2),special_flags=BLEND_RGB_SUB)
```

#### In engine.py

