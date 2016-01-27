import os

from django.conf import settings
from django.http import HttpResponse

from PIL import Image, ImageDraw, ImageFont


def avatar(request, initials):
    size = request.GET.get('size', 128)
    bg = request.GET.get('bg', 'B75582')
    fg = request.GET.get('fg', 'FFFFFF')

    bg = '#{0}'.format(bg)
    fg = '#{0}'.format(fg)

    initials = initials[:2]
    initials = initials.upper()

    avatar_dir = u'{0}/avatar/{1}'.format(settings.MEDIA_ROOT, size)
    avatar_path = u'{0}/{1}.png'.format(avatar_dir, initials)

    if os.path.isfile(avatar_path):
        im = Image.open(avatar_path)
    else:
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
        if not os.path.exists(avatar_dir):
            os.makedirs(avatar_dir)
        im.save(avatar_path, 'png')

    response = HttpResponse(content_type='image/png')
    im.save(response, 'png')
    return response
