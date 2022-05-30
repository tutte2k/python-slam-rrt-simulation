import env
import sensors
import features
import random
import pygame
import math

# def random_color():
#     levels = range(32, 256, 32)
#     return tuple(random.choice(levels)for _ in range(3))


# featureMap = features.FeaturesDetection()
# environment = env.buildEnvironment((600, 1200))
# originalMap = environment.map.copy()
# laser = sensors.LaserSensor(200, originalMap, uncertainty=(0.5, 0.01))
# environment.map.fill((255, 255, 255))
# environment.infoMap = environment.map.copy()
# originalMap = environment.map.copy()
# running = True
# FEATURE_DETECTION = True
# BREAK_POINT_IND = 0

# while running:
#     environment.infoMap = originalMap.copy()
#     FEATURE_DETECTION = True
#     BREAK_POINT_IND = 0
#     ENDPOINTS = [0, 0]
#     sensorOn = False
#     PREDICTED_POINTS_TODRAW = []
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     if pygame.mouse.get_focused():
#         sensorOn = True
#     elif not pygame.mouse.get_focused():
#         sensorOn = False
#     if sensorOn:
#         position = pygame.mouse.get_pos()
#         laser.position = position
#         sensor_data = laser.sense_obstacles()
#         featureMap.setLaserPoints(sensor_data)
#         while BREAK_POINT_IND < (featureMap.NP - featureMap.PMIN):
#             seedSeg = featureMap.seed_segment_detection(
#                 laser.position, BREAK_POINT_IND)
#             if seedSeg == False:
#                 break
#             else:
#                 seedSegment = seedSeg[0]
#                 PREDICTED_POINTS_TODRAW = seedSeg[1]
#                 INDICES = seedSeg[2]
#                 results = featureMap.seed_segment_growing(
#                     INDICES, BREAK_POINT_IND)
#                 if results == False:
#                     BREAK_POINT_IND = INDICES[1]
#                     continue
#                 else:
#                     line_eq = results[1]
#                     m, c = results[5]
#                     line_seg = results[0]
#                     OUTERMOST = results[2]
#                     BREAK_POINT_IND = results[3]
#                     ENDPOINTS[0] = featureMap.projection_point2line(
#                         OUTERMOST[0], m, c)
#                     ENDPOINTS[1] = featureMap.projection_point2line(
#                         OUTERMOST[1], m, c)

#                     COLOR = random_color()
#                     for point in line_seg:
#                         environment.infoMap.set_at(
#                             (int(point[0][0]), int(point[0][1])), (0, 255, 0))
#                         pygame.draw.circle(environment.infoMap, COLOR, (int(
#                             point[0][0]), int(point[0][1])), 2, 0)
#                     pygame.draw.line(environment.infoMap,
#                                      (255, 0, 0), ENDPOINTS[0], ENDPOINTS[1], 2)

#                     environment.dataStorage(sensor_data)
#     environment.map.blit(environment.infoMap, (0, 0))
#     pygame.display.update()





environment = env.buildEnvironment((600, 1200))
environment.originalMap = environment.map.copy()
laser = sensors.LaserSensor(
    200, environment.originalMap, uncertainty=(0.0, 0.01))
environment.map.fill((0, 0, 0))
environment.infoMap = environment.map.copy()

running = True

while running:
    sensorOn = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            sensorOn = True
        elif not pygame.mouse.get_focused():
            sensorOn = False
    if sensorOn:
        position = pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles()
        environment.dataStorage(sensor_data)
        environment.show_sensorData()
    environment.map.blit(environment.infoMap, (0, 0))
    pygame.display.update()
