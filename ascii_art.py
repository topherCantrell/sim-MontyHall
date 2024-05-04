import re

# '|' and '-' are ignored
# ; starts a comment. Everything after it is ignored.
# Sprites are defined in a sheet of rows and columns
# All the sprites on a row must have the same height, but can have different widths


def separate_images(art):
    """separate the art sheet into separate image string arrays
    """
    art = art.replace('|', ' ')  # Ignore visual divider characters
    art = art.replace('-', ' ')  # Ignore visual divider characters
    art = re.sub(' {2,}', ' ', art)  # Collapse multiple white spaces

    # Separate the rows of images from the image sheet
    rows = [[]]
    for line in art.split('\n'):
        if ';' in line:
            line = line[:line.index(';')]
        if not line.strip():
            rows.append([])
        else:
            rows[-1].append(line)
    for i in range(len(rows)-1, -1, -1):
        if not rows[i]:
            del rows[i]

    # Separate the images on a single row of images
    images = []
    for y in rows:
        currow = []
        for row in y:
            s = row.strip().split(' ')
            if not currow:
                for i in range(len(s)):
                    currow.append([])
            for i in range(len(s)):
                currow[i].append(s[i])
        images = images + currow

    return images


def to_pixel_array(art, mapping):
    ret = []
    for row in art:
        ret.append([])
        for col in row:
            ret[-1].append(mapping[col])
    return ret


def to_8x8_bicolor(pixels):
    ret = [0]*16
    for j in range(8):
        for i in range(8):
            dval = pixels[i][j]
            ret[14-j*2] |= (dval & 1) << i
            ret[14-j*2+1] |= ((dval & 2) >> 1) << i
    return ret
