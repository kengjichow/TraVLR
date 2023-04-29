import cv2 as cv
import numpy as np
from Enums import Shapes, Colours, Size
from math import sin, cos, pi
from const import IMAGES_FILEPATH


class ImageGen:
    def __init__(self, height, width, num_rows, num_cols):
        self.img = None
        self.height = height
        self.width = width
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.coord_dic = {}
        self.cell_max_dim = min(height/num_rows, width/num_cols)
        self.get_centers()
        self.image_idx = 0

    def get_centers(self):
        vertical = (self.height/self.num_rows)
        horizontal = (self.width/self.num_cols)
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.coord_dic[(i, j)] = (round(horizontal/2+horizontal*j),
                                          round(vertical/2+vertical*i))
        return self.coord_dic

    def draw_objects(self, object_list):
        self.img = np.full((self.height, self.width, 3), 255, np.uint8)
        for obj in object_list:
            self.draw_shape(obj.shape, (obj.row, obj.column),
                            obj.colour, obj.size)
        return self.img

    def show_image(self):
        cv.imshow('window', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def save_image(self, image_idx=None):
        if image_idx is None:
            image_idx = self.image_idx
        filepath = IMAGES_FILEPATH + str(image_idx) + '.jpg'
        cv.imwrite(filepath, self.img)
        self.image_idx += 1
        return image_idx

    def draw_shape(self, shape, coords, colour, size):
        if shape == Shapes.CIRCLE:
            self.draw_circle(coords, colour, size)
        elif shape == Shapes.TRIANGLE:
            self.draw_polygon(3, coords, colour, size)
        elif shape == Shapes.PENTAGON:
            self.draw_polygon(5, coords, colour, size)
        elif shape == Shapes.HEXAGON:
            self.draw_polygon(6, coords, colour, size)
        elif shape == Shapes.OCTAGON:
            self.draw_polygon(8, coords, colour, size)
        elif shape == Shapes.SQUARE:
            self.draw_square(coords, colour, size)
        elif shape == Shapes.STAR:
            self.draw_star(coords, colour, size)
        elif shape == Shapes.TRAPEZIUM:
            self.draw_trapezium(coords, colour, size)
        elif shape == Shapes.PARALLELOGRAM:
            self.draw_parallelogram(coords, colour, size)

    def draw_circle(self, coords, colour, size):
        radius = int(self.cell_max_dim * Size.get_ratio(size) / 2)
        cv.circle(self.img, self.coord_dic[coords],
                  radius, Colours.rgb(colour), -1)

    # adapted from https://stackoverflow.com/questions/36942995/point-formula-for-polygon/36943401#36943401
    def draw_polygon(self, num_pts, coords, colour, size):
        x, y = self.coord_dic[coords]
        radius = round(self.cell_max_dim * Size.get_ratio(size) / 2)
        points = [(x, y-radius)]
        theta = pi/2
        d_theta = 2*pi/num_pts

        for i in range(1, num_pts):
            theta += d_theta
            points.append((round(x + radius*cos(theta)),
                          round(y - radius*sin(theta))))

        cv.fillPoly(self.img, np.array([points]), Colours.rgb(colour))
        return points

    def draw_square(self, coords, colour, size):
        x, y = self.coord_dic[coords]
        radius = round(self.cell_max_dim * Size.get_ratio(size) / 2)
        points = []
        theta = 3*pi/4
        d_theta = pi/2

        for i in range(0, 4):
            angle = theta + d_theta * i
            points.append((round(x + radius*cos(angle)),
                          round(y - radius*sin(angle))))

        cv.fillPoly(self.img, np.array([points]), Colours.rgb(colour))
        return points

    def draw_parallelogram(self, coords, colour, size):
        x, y = self.coord_dic[coords]
        radius = round(self.cell_max_dim * Size.get_ratio(size) / 2)
        points = []
        theta = 3*pi/4
        d_theta = pi/2

        for i in range(0, 4):
            angle = theta + d_theta * i
            points.append((round(x + radius*cos(angle)),
                          round(y - radius*sin(angle))))
        width = points[2][0] - points[1][0]
        points[0] = (round(points[0][0] + width/3), points[0][1])
        points[2] = (round(points[2][0] - width/3), points[2][1])
        cv.fillPoly(self.img, np.array([points]), Colours.rgb(colour))
        return points

    def draw_trapezium(self, coords, colour, size):
        x, y = self.coord_dic[coords]
        radius = round(self.cell_max_dim * Size.get_ratio(size) / 2)
        points = []
        theta = pi/2
        d_theta = 2*pi/3

        for i in range(1, 3):
            theta += d_theta
            points.append((round(x + radius*cos(theta)),
                          round(y - radius*sin(theta))))
        points.append((round(x-(points[0][0]-x)/2), y-radius))
        points.append((round(x+(points[0][0]-x)/2), y-radius))

        cv.fillPoly(self.img, np.array([points]), Colours.rgb(colour))
        return points

    def draw_star(self, coords, colour, size):
        x, y = self.coord_dic[coords]
        inner_radius = int(self.cell_max_dim * Size.get_ratio(size) / 4)
        outer_radius = int(self.cell_max_dim * Size.get_ratio(size) / 2)
        points = []
        outer_theta = pi/2
        d_theta = 2*pi/5

        inner_theta = pi/2 + 2*pi/10

        for i in range(0, 5):
            angle = outer_theta + d_theta * i
            points.append((round(x + outer_radius*cos(angle)),
                          round(y - outer_radius*sin(angle))))
            angle = inner_theta + d_theta * i
            points.append((round(x + inner_radius*cos(angle)),
                          round(y - inner_radius*sin(angle))))

        cv.fillPoly(self.img, np.array([points]), Colours.rgb(colour))
        return points
