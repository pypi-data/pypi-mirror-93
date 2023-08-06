#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the garoupa project.
#  Please respect the license - more about this in the section (*) below.
#
#  garoupa is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  garoupa is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with garoupa.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# configuration
width = 158
height = 176
font_size = 48
start_limit = 150
limit = 200
inc = 15
offset = 200


def move(fc, aft):
    r, g, b = fc
    dr = (r + inc) % limit if r < round((limit * ord(aft[0]) / 800)) else (r + limit - inc) % limit
    dg = (g + inc) % limit if g < round((limit * ord(aft[1]) / 800)) else (r + limit - inc) % limit
    db = (b + inc) % limit if b < round((limit * ord(aft[2]) / 800)) else (r + limit - inc) % limit
    return dr, dg, db


def avatar(uuid, f="uuid-avatar-$id.jpg"):
    """Generate a colorful image.

    <$id> at the filename will be replaced by the provided uuid."""
    if "$id" in f:
        f.replace("$id", uuid)
    n = uuid.n
    tt = " " + uuid.id

    res, c1 = divmod(n, 21780986680939)
    res, c2 = divmod(res, 21780986680939)
    _, c3 = divmod(res, 21780986680939)
    b1, b2, b3 = (
        offset + round((255 - offset) * c1 / 21780986680939),
        offset + round((255 - offset) * c2 / 21780986680939),
        offset + round((255 - offset) * c3 / 21780986680939),
    )
    back_ground_color = b1, b2, b3

    im = Image.new("RGB", (width, height), back_ground_color)
    draw = ImageDraw.Draw(im)
    unicode_font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", font_size)

    res, rem = divmod(c1, 27928)
    r = round(start_limit * rem / 27928)
    res, rem = divmod(res, 27928)
    g = round(start_limit * rem / 27928)
    res, rem = divmod(res, 27928)
    b = round(start_limit * rem / 27928)
    font_color = r, g, b
    c = 0
    i = 0
    for l in tt[0:5]:
        draw.text((3 + i, 3), l, font=unicode_font, fill=font_color)
        i += 31
        c += 1
        font_color = move(font_color, tt[c:c + 3])

    res, rem = divmod(c2, 27928)
    r = round(start_limit * rem / 27928)
    res, rem = divmod(res, 27928)
    g = round(start_limit * rem / 27928)
    res, rem = divmod(res, 27928)
    b = round(start_limit * rem / 27928)
    font_color = r, g, b
    c = 0
    i = 0
    for l in tt[5:10]:
        draw.text((3 + i, 61), l, font=unicode_font, fill=font_color)
        i += 31
        c += 1
        font_color = move(font_color, tt[c:c + 3])

    res, rem = divmod(c3, 27928)
    r = round(start_limit * rem / 27928)
    res, rem = divmod(res, 27928)
    g = round(start_limit * rem / 27928)
    res, rem = divmod(res, 27928)
    b = round(start_limit * rem / 27928)
    font_color = r, g, b
    c = 0
    i = 0
    for l in tt[10:15]:
        draw.text((3 + i, 117), l, font=unicode_font, fill=font_color)
        i += 31
        c += 1
        font_color = move(font_color, tt[c:c + 3])
        # if c == 13:
        #     font_color = move(font_color, tt[13:15] + tt[1])
        # else:
        #     font_color = move(font_color, tt[14] + tt[1:3])

    im.save(f)
