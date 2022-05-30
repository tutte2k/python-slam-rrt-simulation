import math
import pygame


class buildEnvironment:
    def __init__(self, mapDimensions):
        pygame.init()
        self.pointCloud = []
        self.externalMap = pygame.image.load('map1.png')
        self.maph, self.mapw = mapDimensions
        self.mapWindowName = 'RRT Path Planning'
        pygame.display.set_caption(self.mapWindowName)
        self.map = pygame.display.set_mode((self.mapw, self.maph))
        self.map.blit(self.externalMap, (0, 0))
        # colors
        self.black = (0, 0, 0)
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)

    def Ad2Pos(self, distance, angle, robotPosition):
        x = distance * math.cos(angle)+robotPosition[0]
        y = -distance * math.sin(angle)+robotPosition[1]
        return (int(x), int(y))

    def dataStorage(self, data):
        print(len(self.pointCloud))
        if data:
            for element in data:
                point = self.Ad2Pos(element[0], element[1], element[2])
                if point not in self.pointCloud:
                    self.pointCloud.append(point)

    def show_sensorData(self):
        self.infoMap = self.map.copy()
        for point in self.pointCloud:
            self.infoMap.set_at((int(point[0]), int(point[1])), (255, 0, 0))
