def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()


def message_display(display, x, y, text, font, colour):
    TextSurf, TextRect = text_objects(text, font, colour)
    TextRect.center = (x, y)
    display.blit(TextSurf, TextRect)
