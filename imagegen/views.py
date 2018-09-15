import random, os

from django.http import HttpResponse, HttpResponseBadRequest
from django import forms
from io import BytesIO
from PIL import Image, ImageDraw
import json

from . import models


class ImagegenForm(forms.Form):
    width = forms.IntegerField(min_value=1, max_value=1500)
    height = forms.IntegerField(min_value=1, max_value=1500)

    def generate(self, mandelbrot=False, image_format='PNG'):
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        image = Image.new('RGB', (width, height))
        if mandelbrot:
            image = self.mandelbrot(image)
        content = BytesIO()
        image.save(content, image_format)
        content.seek(0)
        return content


    def mandelbrot(self, image):
        # size of the draw size
        xa = -0.75
        xb = 0.75
        ya = -0.75
        yb = 0.75

        # maximum number of iterations
        num_iterations = random.randint(50, 100)  # max iterations allowed

        # image size
        width = self.cleaned_data['width']
        height = self.cleaned_data['height']
        c = complex(random.random() * 2.0 - 1.0, random.random() - 0.5)

        # generate the fractal
        for y in range(height):
            zy = y * (yb - ya) / (height - 1) + ya
            for x in range(width):
                zx = x * (xb - xa) / (width - 1) + xa
                z = complex(zx, zy)
                for i in range(num_iterations):
                    if abs(z) > 2.0: break
                    z = z * z + c
                r = i % 4 * 64
                g = i % 8 * 32
                b = i % 16 * 16
                image.putpixel((x, y), b * 65536 + g * 256 + r)
        return image


def absolute_image_slug(slug):
    path = "%s/static/imagegen" % os.path.dirname(__file__)
    absolute_slug = "%s/%s" % (path, slug)
    return absolute_slug


def save_image_record(image, dimensions, category):
    save_image = models.GeneratedImage()
    save_image.slug = ""
    save_image.width, save_image.height = dimensions
    save_image.save()

    save_image.slug = "%s_image_%d" % (category, save_image.id)
    save_image.save()

    save_image_file(image, save_image.slug)

    return save_image.slug


def save_image_file(image, slug):
    path = os.path.dirname(__file__)
    with open("%s/static/imagegen/%s" % (path, slug), "wb") as f:
        f.write(image.read())


def simple(request, width=0, height=0):
    form = ImagegenForm({'width': width, 'height': height})
    if form.is_valid():
        image = form.generate(mandelbrot=False)
        slug = save_image_record(image, [width, height], 'simple')
        return HttpResponse(json.dumps({
            'url': slug,
            'aspect_ratio': float(width) / float(height)
        }), 'application/json')
    return HttpResponseBadRequest("Invalid image request")


def mandelbrot(request, width=0, height=0):
    form = ImagegenForm({'width': width, 'height': height})
    if form.is_valid():
        image = form.generate(mandelbrot=True)
        slug = save_image_record(image, [width, height], 'mandelbrot')
        return HttpResponse(json.dumps({
            'url': slug,
            'aspect_ratio': float(width) / float(height)
        }), 'application/json')
    return HttpResponseBadRequest("Invalid image request")


def saved_image(request, slug=''):
    image = BytesIO()
    path = absolute_image_slug(slug)
    with open(path, "rb") as f:
        image.write(f.read())
    image.seek(0)
    return HttpResponse(image, 'image/png')
