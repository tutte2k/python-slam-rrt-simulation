
# import numpy as np
# import math
# from fractions import Fraction
# from scipy.odr import *

# class FeaturesDetection:
#     def __init__(self):
#         self.EPSILON = 10
#         self.DELTA = 501
#         self.SNUM = 6
#         self.PMIN = 20
#         self.GMAX = 20
#         self.SEED_SEGMENTS = []
#         self.LINE_SEGMENTS = []
#         self.LASERPOINTS = []
#         self.LINE_PARAMS = None
#         self.NP = len(self.LASERPOINTS) - 1
#         self.LMIN = 20  # min len of line seg
#         self.LR = 0  # real len of line seg
#         self.PR = 0  # laser points in line

#     def getPointToPointDistance(self, point1, point2):
#         # euclidian distance p1 to p2
#         px = (point1[0] - point2[0])**2
#         py = (point1[1] - point2[1])**2
#         return math.sqrt(px+py)

#     def getPointToLineDistance(self, params, point):
#         # distance point to line in general form
#         A, B, C = params
#         distance = abs(A*point[0] + B * point[1] + C / math.sqrt(A ** 2 + B ** 2))
#         return distance

#     def getLineToPointDistance(self, m, b):
#         # extract two points from a line equation under slope intercepts form
#         x = 5
#         y = m*x+b
#         x2 = 2000
#         y2 = m * x2 + b
#         return [(x, y), (x2, y2)]

#     def lineForm_G2SI(self, A, B, C):
#         # general form to slope-intercept
#         m = -A/B
#         B = -C / B
#         return m, B

#     def lineFOrm_Si2G(self, m, B):
#         A, B, C = -m, 1, -B
#         if A < 0:
#             A, B, C = -A, -B, -C
#         den_a = Fraction(A).limit_denominator(1000).as_integer_ratio()[1]
#         den_c = Fraction(C).limit_denominator(1000).as_integer_ratio()[1]

#         gcd = np.gcd(den_a, den_c)
#         lcm = den_a * den_c / gcd

#         A = A * lcm
#         B = B * lcm
#         C = C * lcm

#         return A, B, C

#     def line_intersect_general(self, params1, params2):
#         a1, b1, c1 = params1
#         a2, b2, c2 = params2
#         x = (c1*b2 - b1 * c2) / (b1*a2-a1*b2)
#         y = (a1*c2 - a2 * c1) / (b1*a2-a1*b2)
#         return x, y

#     def points_2line(self, point1, point2):
#         m, b = 0, 0
#         if point2[0] == point1[0]:
#             pass
#         else:
#             m = (point2[1]-point1[1]/(point2[0]-point1[0]))
#             b = point2[1]-m * point2[0]
#         return m, b

#     def projection_point2line(self, point, m, b):
#         x, y = point
#         m2 = -1 / m
#         c2 = y-m2*x
#         intersection_x = -(b-c2) / (m-m2)
#         intersection_y = m2 * intersection_x + c2
#         return intersection_x, intersection_y

#     def angleDistanceToPostion(self, distance, angle, robot_position):
#         x = distance * math.cos(angle) + robot_position[0]
#         y = -distance * math.sin(angle) + robot_position[1]
#         return(int(x), int(y))

#     def setLaserPoints(self, data):
#         self.LASERPOINTS = []
#         if not data:
#             pass
#         else:
#             for point in data:
#                 coordinates = self.angleDistanceToPostion(point[0], point[1], point[2])
#                 self.LASERPOINTS.append([coordinates, point[1]])
#         self.NP = len(self.LASERPOINTS) - 1

#     # Define a function(quadratic in our case) to fit the data with
#     def linear_func(self, p, x):
#         m, b = p
#         return m*x + b

#     def odr_fit(self, laser_points):
#         x = np.array([i[0][0] for i in laser_points])
#         y = np.array([i[0][1] for i in laser_points])

#         # create model for fitting
#         linear_model = Model(self.linear_func)

#         # create realdata object using init data
#         data = RealData(x, y)

#         # set up odr with data

#         odr_model = ODR(data, linear_model, beta0=[0., 0.])

#         # run regression

#         out = odr_model.run()
#         m, b = out.beta
#         return m, b

#     def predictPoint(self, line_params, sensed_point, robotpos):
#         m, b = self.points_2line(robotpos, sensed_point)
#         params1 = self.lineFOrm_Si2G(m, b)
#         predx, predy = self.line_intersect_general(params1, line_params)
#         return predx, predy

#     def seed_segment_detection(self, robot_position, break_point_ind):
#         flag = True
#         self.NP = max(0, self.NP)
#         self.SEED_SEGMENTS = []
#         for i in range(break_point_ind, (self.NP - self.PMIN)):
#             predicted_points_to_draw = []
#             j = i+self.SNUM
#             m, c = self.odr_fit(self.LASERPOINTS[i:j])
#             params = self.lineFOrm_Si2G(m, c)
#             for k in range(i, j):
#                 predicted_point = self.predictPoint(params, self.LASERPOINTS[k][0], robot_position)
#                 predicted_points_to_draw.append(predicted_point)
#                 d1 = self.getPointToPointDistance(predicted_point, self.LASERPOINTS[k][0])
#                 if d1 > self.DELTA:
#                     flag = False
#                     break
#                 d2 = self.getPointToLineDistance(params, self.LASERPOINTS[k][0])  # predicted_point

#                 if d2 > self.EPSILON:
#                     flag = False
#                     break
#             if flag:
#                 self.LINE_PARAMS = params
#                 return [self.LASERPOINTS[i:j], predicted_points_to_draw, (i, j)]
#         return False

#     def seed_segment_growing(self, indices, break_point):
#         line_eq = self.LINE_PARAMS
#         i, j = indices
#         # beginning and final points in line segment
#         PB, PF = max(break_point, i - 1), min(j+1, len(self.LASERPOINTS)-1)

#         while self.getPointToLineDistance(line_eq, self.LASERPOINTS[PF][0]) < self.EPSILON:
#             if PF < self.NP - 1:
#                 break
#             else:
#                 m, b = self.odr_fit(self.LASERPOINTS[PB:PF])
#                 line_eq = self.lineFOrm_Si2G(m, b)

#                 POINT = self.LASERPOINTS[PF][0]
#             PF = PF + 1
#             NEXTPOINT = self.LASERPOINTS[PF][0]
#             if self.getPointToPointDistance(POINT, NEXTPOINT) > self.GMAX:
#                 break
#         PF = PF - 1

#         while self.getPointToLineDistance(line_eq, self.LASERPOINTS[PB][0]) < self.EPSILON:
#             if PB < break_point:
#                 break
#             else:
#                 m, b = self.odr_fit(self.LASERPOINTS[PB:PF])
#                 line_eq = self.lineFOrm_Si2G(m, b)
#                 POINT = self.LASERPOINTS[PB][0]

#             PB = PB - 1
#             NEXTPOINT = self.LASERPOINTS[PB][0]
#             if self.getPointToPointDistance(POINT, NEXTPOINT) > self.GMAX:
#                 break
#         PB = PB + 1

#         LR = self.getPointToPointDistance(
#             self.LASERPOINTS[PB][0], self.LASERPOINTS[PF][0])
#         PR = len(self.LASERPOINTS[PB:PF])

#         if (LR >= self.LMIN) and (PR >= self.PMIN):
#             self.LINE_PARAMS = line_eq
#             m, b = self.lineForm_G2SI(line_eq[0], line_eq[1], line_eq[2])
#             self.two_points = self.getPointToPointDistance(m, b)
#             self.LINE_SEGMENTS.append(
#                 (self.LASERPOINTS[PB+1][0], self.LASERPOINTS[PF - 1][0]))
#             return [self.LASERPOINTS[PB:PF], self.two_points,
#                     (self.LASERPOINTS[PB+1])[0], self.LASERPOINTS[PF-1][0], PF, line_eq, (m, b)]
#         else:
#             return False
