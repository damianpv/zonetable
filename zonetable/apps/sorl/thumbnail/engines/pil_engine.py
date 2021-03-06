from cStringIO import StringIO
from zonetable.apps.sorl.thumbnail.engines.base import EngineBase

try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw


class Engine(EngineBase):
    def get_image(self, source):
        buf = StringIO(source.read())
        return Image.open(buf)

    def get_image_size(self, image):
        return image.size

    def dummy_image(self, width, height):
        d = self._get_dummy_image_data(width, height)
        im = Image.new('RGB', (width, height), d['canvas_color'])
        draw = ImageDraw.Draw(im)
        for line in d['lines']:
            draw.line(line, fill=d['line_color'])
        draw.rectangle(d['rectangle'], outline=d['line_color'])
        del draw
        return im

    def is_valid_image(self, raw_data):
        buf = StringIO(raw_data)
        try:
            trial_image = Image.open(buf)
            trial_image.verify()
        except Exception:
            return False
        return True

    def _colorspace(self, image, colorspace):
        if colorspace == 'RGB':
            if image.mode == 'RGBA':
                return image # RGBA is just RGB + Alpha
            if image.mode == 'P' and 'transparency' in image.info:
                return image.convert('RGBA')
            return image.convert('RGB')
        if colorspace == 'GRAY':
            return image.convert('L')
        return image

    def _scale(self, image, width, height):
        return image.resize((width, height), resample=Image.ANTIALIAS)

    def _crop(self, image, width, height, x_offset, y_offset):
        return image.crop((x_offset, y_offset,
                           width + x_offset, height + y_offset))

    def _get_raw_data(self, image, format_, quality):
        Image.MAXBLOCK = 1024 * 1024
        buf = StringIO()
        try:
            image.save(buf, format=format_, quality=quality, optimize=1)
        except IOError:
            image.save(buf, format=format_, quality=quality)
        raw_data = buf.getvalue()
        buf.close()
        return raw_data

