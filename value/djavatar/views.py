from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
import os

def avatar(request, initials):
    size = request.GET.get('size', 128)
    bg = request.GET.get('bg', 'B75582')
    fg = request.GET.get('fg', 'FFFFFF')

    bg = '#{0}'.format(bg)
    fg = '#{0}'.format(fg)

    initials = initials[:2]
    initials = initials.upper()

    try:
        size = int(size)
    except Exception, e:
        size = 128

    W, H = (size,size)
    im = Image.new('RGB', (W,H), bg)
    draw = ImageDraw.Draw(im)
    font_path = '{0}/font/{1}'.format(os.path.dirname(__file__), 'SourceCodePro-Bold.ttf')
    font = ImageFont.truetype(font_path, size/2)
    w, h = draw.textsize(initials, font=font)
    draw.text(((W-w)/2, (W-w)/2), initials, fill=fg, font=font)    
    del draw
    response = HttpResponse(content_type='image/png')
    im.save(response, 'PNG')
    return response
