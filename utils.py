import pygame 
# we need access to pygame to use this fucntino 

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    # # need to figure out its x and y position by stating the top left hand corner of that image is equal to the x and y position and from there get the center of that and where the center of that image is and the new image still needs to be on that center so we can rotate from the center of the image and now from the corner
    win.blit(rotated_image, new_rect.topleft)

def blit_text_center(win, font, text1,text2):
    render = font.render(text1, 1, (0, 0, 0))
    render2 = font.render(text2, 1, (0, 0, 0))

    pygame.draw.rect(win, (255,255,255), (0,(win.get_height()/2)-100,win.get_width(), 200))

    #  putting in the text we want to enter, the anti alliasing (usally just keep at 1), and the colour of text we want (made it grey)
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))
    win.blit(render2, (win.get_width()/2 - render2.get_width()/2, win.get_height()/2 - render2.get_height()/2 + render.get_height()))
