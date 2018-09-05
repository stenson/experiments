from random import random, randint

def rasterize(glyph, cellSize=50, xMin=None, yMin=None, xMax=None, yMax=None):
    """
    Slice the glyph into a grid based on the given cell size.

    Returns a list of lists containing bool values that indicate the
    black (True) or white (False) value of that particular cell.
    These lists are arranged from top to bottom of the glyph and proceed
    from left to right.

    Warning: This is an expensive operation!
    """

    if xMin is None or yMin is None or xMax is None or yMax is None:
        _xMin, _yMin, _xMax, _yMax = glyph.bounds()
        if xMin is None:
            xMin = _xMin
        if yMin is None:
            yMin = _yMin
        if xMax is None:
            xMax = _xMax
        if yMax is None:
            yMax = _yMax

    hitXMax = False
    hitYMin = False
    xSlice = 0
    ySlice = 0
    halfCellSize = cellSize / 2.0
    bitmap = []

    while not hitYMin:
        bitmap.append([])
        yScan = -(ySlice * cellSize) + yMax - halfCellSize
        if yScan < yMin:
            hitYMin = True
        while not hitXMax:
            xScan = (xSlice * cellSize) + xMin - halfCellSize
            if xScan > xMax:
                hitXMax = True
            test = glyph.pointInside((xScan, yScan))
            if test:
                bitmap[-1].append(True)
            else:
                bitmap[-1].append(False)
            xSlice = xSlice + 1
        hitXMax = False
        xSlice = 0
        ySlice = ySlice + 1
    return bitmap

offset = (150, 50)
fs = FormattedString()
fs.font("Urushi v0.1")
fs.fontSize(900)
fs.append("鷹")
bp = BezierPath()
bp.text(fs, offset)
fill(0)
rect(0, 0, width(), height())
fill(1, 1, 0, 0.5)
#drawPath(bp)

# rasterize the current glyph
raster_size = 3
bitmap = rasterize(bp, raster_size)

def randshift():
    #return 0
    return randint(0, 2) - 1

def draw_pixels():
    for y, line in enumerate(bitmap):
        for x, bit in enumerate(line):
            if bit:
                yscore = 0
                searching = True
                py = y - 1
                while searching and py >= 0:
                    prev = bitmap[py][x]
                    if prev:
                        py = py - 1
                        yscore += 1
                    else:
                        searching = False
                
                xscore = 0
                searching = True
                px = x - 1
                while searching and px >= 0:
                    prev = bitmap[y][px]
                    if prev:
                        px = px - 1
                        xscore += 1
                    else:
                        searching = False
                
                #print(x, y, yscore, xscore)
                
                score = yscore + xscore
                # draw = True
                # if score == 0 or score == 1:
                #     draw = random() < 0.2
                # else:
                #     draw = random() > (1/(score/6))
                
                if xscore < 4 or yscore < 4:
                    draw = random() > 0.9
                elif xscore < 10 or yscore < 10:
                    draw = random() > 0.7
                elif xscore < 20 or yscore < 20:
                    draw = random() > 0.5
                elif score > 80:
                    draw = random() < 0.9
                elif score > 60 / raster_size:
                    draw = random() > 0.2
                else:
                    draw = random() > 0.7
                
                if draw:
                    fill(1, 1, 1, pow(random(), 0.2)) #0.5 + pow(random(), 2)/0.5)
                    oval(x * raster_size + offset[0] + 65 + randshift(), height() - (y * raster_size + offset[1]) - 18 + randshift(), raster_size + 1, raster_size + 1)

draw_pixels()