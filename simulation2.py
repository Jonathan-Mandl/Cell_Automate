import subprocess
import pkg_resources
import sys
import os

# check if the packages being used are installed and if not- install
packages = {'matplotlib', 'numpy', 'pygame', 'easygui'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = packages - installed
if missing:
    print('Download dependencies here: ', os.getcwd())
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

import copy
import random
import matplotlib.pyplot as plt
import numpy as np
from itertools import product
from random import sample
import pygame
from easygui import multenterbox

P = 0.5  # Population density - P (0-1)
S1 = 25  # The percentage of people who believe every rumor - S1 (0-100)
S2 = 25  # The percentage of people whose basic probability they believe rumors is 2/3 - S2 (0-100)
S3 = 25  # The percentage of people whose basic probability they believe rumors is 1/3 - S3 (0-100)
S4 = 25  # The percentage of people who don't believe any rumor - S4 (0-100)
L = 3  # The number of generations in which a rumor is not spread by a person who spread it - L (0-1000)
mat_size = 100
max_generation = 50
wrap_around_hor = True
wrap_around_ver = True
diagonaly = False
num_of_cells = mat_size * mat_size

slategrey = (112, 128, 144)  # slategrey
lightgrey = (165, 175, 185)  # lightgrey
blackish = (10, 10, 10)  # blackish
empty_cell_color = (255, 255, 255)  # white
manned_cell_color = (0, 0, 0)  # black

people_exposed = []
total_people = []
percent_exposed = []
num_people_exposed = []
white = (255, 255, 255)
black = (0, 0, 0)


def input_check(parameters):
    flag = True
    if len(parameters) < 7:
        print("num args")
        flag = False
    else:
        P, S1, S2, S3, S4, L, max_generation = parameters
        input = []
        input.append(P)
        input.append(S1)
        input.append(S2)
        input.append(S3)
        input.append(S4)
        input.append(L)
        input.append(max_generation)

        for i in range(7):
            if input[i] == '':
                input[i] = "0"

        i = 0

        # Population density - P
        P = globals()['P'] = float(input[i])
        i += 1
        # The percentage of people who believe every rumor - S1
        S1 = globals()['S1'] = int(input[i])
        i += 1
        # The percentage of people whose basic probability they believe rumors is 2/3 - S2
        S2 = globals()['S2'] = int(input[i])
        i += 1
        # The percentage of people whose basic probability they believe rumors is 1/3 - S3
        S3 = globals()['S3'] = int(input[i])
        i += 1
        # The percentage of people who don't believe any rumor - S4
        S4 = globals()['S4'] = int(input[i])
        i += 1
        # number of generations in which a rumor is not spread by a person who spread it - L
        L = globals()['L'] = int(input[i])
        i += 1
        max_generation = globals()['max_generation'] = int(max_generation)

        if float(P) <= 0 or float(P) > 1:
            print("p problem")
            flag = False
        elif int(S1) < 0 or int(S1) > 100:
            print("S1 problem")
            flag = False
        elif int(S2) < 0 or int(S2) > 100:
            print("S2 problem")
            flag = False
        elif int(S3) < 0 or int(S3) > 100:
            print("S3 problem")
            flag = False
        elif int(S4) < 0 or int(S4) > 100:
            print("S4 problem")
            flag = False
        elif int(L) < 0:
            print("L problem")
            flag = False
        elif int(S1) + int(S2) + int(S3) + int(S4) != 100:
            print("percentage problem")
            flag = False

    return flag


class People:
    def __init__(self, rows, columns, doubt):
        self.row = rows
        self.column = columns
        self.base_doubt = doubt
        self.current_doubt = doubt
        self.num_generations = 0
        self.heard = False

    def get_coordinates(self):
        return self.row, self.column

    def set_num_generations(self):
        self.num_generations = L

    def decrease_num_generations(self):
        if self.num_generations > 0:
            self.num_generations -= 1

    def get_doubt(self):
        return self.current_doubt

    def decrease_doubt(self):
        if self.base_doubt == 'S4':
            self.current_doubt = 'S3'
        if self.base_doubt == 'S3':
            self.current_doubt = 'S2'
        if self.base_doubt == 'S2':
            self.current_doubt = 'S1'

    def return_doubt(self):
        self.current_doubt = self.base_doubt

    def can_spread_rumor(self):
        return self.num_generations == 0

    def pass_rumor(self):
        self.heard = True

    def heard_rumor(self):
        return self.heard


def initialize(mat):
    num_of_people = int(P * (mat_size * mat_size))
    num_of_S1 = int(num_of_people * S1 / 100)
    num_of_S2 = int(num_of_people * S2 / 100)
    num_of_S3 = int(num_of_people * S3 / 100)
    num_of_S4 = int(num_of_people * S4 / 100)

    global total_people

    # create a nX2 array of random values for the people
    people_free_location = sample(list(product(range(mat_size), repeat=2)), k=num_of_people)

    for S1_people in range(num_of_S1):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S1')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S2_people in range(num_of_S2):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S2')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S3_people in range(num_of_S3):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S3')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S4_people in range(num_of_S4):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S4')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    return mat

def initializePart2(mat):
    num_of_people = int(P * (num_of_cells))
    num_of_S1 = int(num_of_people * S1 / 100)
    num_of_S2 = int(num_of_people * S2 / 100)
    num_of_S3 = int(num_of_people * S3 / 100)
    num_of_S4 = int(num_of_people * S4 / 100)

    global total_people

    # create a nX2 array of random values for the people
    people_free_location = sample(list(product(range(mat_size), repeat=2)), k=num_of_people)

    S3_line = False
    S3_row = 0
    S3_col = 0
    full_line = False
    col_turn = False
    row_turn = True

    for S3_people in range(num_of_S3):
        location = (row, column) = random.choice(people_free_location)
        if S3_line:
            if row_turn:
                for i in range(mat_size):
                    full_line = True
                    if (S3_row, i) in people_free_location:
                        location = (row, column) = (S3_row, i)
                        full_line = False
                        break
            elif col_turn:
                for i in range(mat_size):
                    full_line = True
                    if (i, S3_col) in people_free_location:
                        location = (row, column) = (i, S3_col)
                        full_line = False
                        break
        S3_line = True
        if full_line:
            S3_line = False
            full_line = False
            col_turn = not col_turn
            row_turn = not row_turn

        S3_row = row
        S3_col = column

        person = People(row, column, 'S3')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S1_people in range(num_of_S1):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S1')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S2_people in range(num_of_S2):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S2')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S4_people in range(num_of_S4):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S4')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    return mat

def initializePart1(mat):
    num_of_people = int(P * (num_of_cells))
    num_of_S1 = int(num_of_people * S1 / 100)
    num_of_S2 = int(num_of_people * S2 / 100)
    num_of_S3 = int(num_of_people * S3 / 100)
    num_of_S4 = int(num_of_people * S4 / 100)

    global total_people

    # create a nX2 array of random values for the people
    people_free_location = sample(list(product(range(mat_size), repeat=2)), k=num_of_people)

    S4_line = False
    S4_row = 0
    S4_col = 0
    full_line = False
    col_turn = False
    row_turn = True

    for S4_people in range(num_of_S4):
        location = (row, column) = random.choice(people_free_location)
        if S4_line:
            if row_turn:
                for i in range(mat_size):
                    full_line = True
                    if (S4_row, i) in people_free_location:
                        location = (row, column) = (S4_row, i)
                        full_line = False
                        break
            elif col_turn:
                for i in range(mat_size):
                    full_line = True
                    if (i, S4_col) in people_free_location:
                        location = (row, column) = (i, S4_col)
                        full_line = False
                        break
        S4_line = True
        if full_line:
            S4_line = False
            full_line = False
            col_turn = not col_turn
            row_turn = not row_turn

        S4_row = row
        S4_col = column

        person = People(row, column, 'S4')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S1_people in range(num_of_S1):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S1')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S2_people in range(num_of_S2):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S2')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    for S3_people in range(num_of_S3):
        location = (row, column) = random.choice(people_free_location)
        person = People(row, column, 'S3')
        mat[row][column] = person
        people_free_location.remove(location)
        total_people.append(person)

    return mat


def edge_behavior(nr, nc):
    if wrap_around_hor:
        nr = nr % mat_size
    else:
        nr = max(nr, 0)
        nr = min(nr, mat_size - 1)

    if wrap_around_ver:
        nc = nc % mat_size
    else:
        nc = max(nc, 0)
        nc = min(nc, mat_size - 1)

    return nr, nc


def neighbors_coordinates(row, col):
    neighbors = []
    neighbors.append((row + 1, col))
    neighbors.append((row - 1, col))
    neighbors.append((row, col + 1))
    neighbors.append((row, col - 1))
    if diagonaly:
        neighbors.append((row + 1, col + 1))
        neighbors.append((row + 1, col - 1))
        neighbors.append((row - 1, col - 1))
        neighbors.append((row - 1, col + 1))

    return neighbors


def spread_rumor(mat, distributors):
    """
    :param mat: matrix of people
    :param distributors: list of people who received rumor in last generation
    :return: list of people who will recieve rumor in this generation
    """
    global people_exposed, total_people
    # get the locations of the neighbors
    doubt_level = {'S1': 1, 'S2': (2 / 3), 'S3': (1 / 3), 'S4': 0}

    # list of people
    rumor_recievers = []
    new_distributors = []

    for person in total_people:
        person.decrease_num_generations()
        person.return_doubt()

    # loop for spreading rumor
    for person in distributors:
        person.set_num_generations()
        row, col = person.get_coordinates()

        # iterate through neighbors. pass rumor.
        for neighbor_coordinates in neighbors_coordinates(row, col):
            # wrap around or not
            nr, nc = edge_behavior(neighbor_coordinates[0], neighbor_coordinates[1])
            # check matrix contains person in this row,column
            if mat[nr, nc] is not None:
                neighbor = mat[nr, nc]
                # check if neighbor did not recieve rumor in this generation already
                if neighbor not in rumor_recievers:
                    rumor_recievers.append(neighbor)
                    neighbor.pass_rumor()
                # if he already recieved rumor, decrease doubt level
                else:
                    neighbor.decrease_doubt()

                if neighbor not in people_exposed:
                    people_exposed.append(neighbor)

    for person in rumor_recievers:
        if person.can_spread_rumor():
            # check person doubt category
            category = person.get_doubt()
            # check person's probability of believing rumor.
            prob = doubt_level[category]
            # ensure person passes rumor in probability according to his doubt level
            if np.random.uniform(0, 1) <= prob:
                new_distributors.append(person)

    return new_distributors


def update_percentage():
    global people_exposed, percent_exposed, num_people_exposed

    num_of_people = int(P * (mat_size * mat_size))
    percentage = len(people_exposed) * 100 / num_of_people
    percent_exposed.append(percentage)
    num_people_exposed.append(len(people_exposed))


def show_params(screen):
    # create text for display
    # font
    font = pygame.font.SysFont('Arial', 15)
    parameters_txt = font.render(
        f'Simulation params: P = {P},   L = {L},    S1 = {S1},  S2 = {S2},  S3 = {S3},  S4 = {S4}'
        , True, slategrey)
    # show text (image variable,(left, top))
    screen.blit(parameters_txt, (5, 0))


def show_legend1(screen, width, legend_height):
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 60)
    BLUE = (0, 0, 255)

    # Draw the legend
    legend_rect = pygame.Rect(0, 0, width, legend_height)
    pygame.draw.rect(screen, WHITE, legend_rect)

    # Draw the legend rectangles
    red_rect = pygame.Rect(10, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, RED, red_rect)

    yellow_rect = pygame.Rect(130, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, YELLOW, yellow_rect)

    grey_rect = pygame.Rect(250, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, lightgrey, grey_rect)

    black_rect = pygame.Rect(370, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, black, black_rect)

    # Draw the legend text labels
    font = pygame.font.SysFont('Arial', 17)
    legend_text = font.render('Legend:', True, black)
    legend_text_rect = legend_text.get_rect(center=(width / 2, 30))
    screen.blit(legend_text, legend_text_rect)

    font = pygame.font.SysFont('Arial', 13)
    red_text = font.render('past spreaders', True, black)
    red_text_rect = red_text.get_rect(center=(red_rect.right+40, legend_height / 2 + 30))
    screen.blit(red_text, red_text_rect)

    yellow_text = font.render('now spreaders', True, black)
    yellow_text_rect = yellow_text.get_rect(center=(yellow_rect.right + 40, legend_height / 2 + 30))
    screen.blit(yellow_text, yellow_text_rect)

    grey_text = font.render('Empty Cell', True, black)
    grey_text_rect = grey_text.get_rect(center=(grey_rect.right + 30, legend_height / 2 + 30))
    screen.blit(grey_text, grey_text_rect)

    black_text = font.render('unheared person', True, black)
    black_text_rect = black_text.get_rect(center=(black_rect.right + 50, legend_height / 2 + 30))
    screen.blit(black_text, black_text_rect)


def show_legend2(screen, width, legend_height):
    WHITE = (255, 255, 255)
    S1_color = (255, 0, 0)
    S2_color = (0, 255, 0)
    S3_color = (0, 0, 255)
    S4_color = (100, 100, 100)

    legend_rect = pygame.Rect(0, 0, width, legend_height)
    pygame.draw.rect(screen, WHITE, legend_rect)

    # Draw the legend rectangles
    S1_rect = pygame.Rect(10, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, S1_color, S1_rect)

    S2_rect = pygame.Rect(80, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, S2_color, S2_rect)

    S3_rect = pygame.Rect(150, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, S3_color, S3_rect)

    S4_rect = pygame.Rect(220, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, S4_color, S4_rect)

    starter = pygame.Rect(290, legend_height / 2 + 20, 20, 20)
    pygame.draw.rect(screen, (205, 255, 255), starter)

    # Draw the legend text labels
    font = pygame.font.SysFont('Arial', 15)
    legend_text = font.render('Legend:', True, black)
    legend_text_rect = legend_text.get_rect(center=(width / 2, 30))
    screen.blit(legend_text, legend_text_rect)

    S1_text = font.render('S1', True, black)
    S1_text_rect = S1_text.get_rect(center=(S1_rect.right + 20, legend_height / 2 + 30))
    screen.blit(S1_text, S1_text_rect)

    S2_text = font.render('S2', True, black)
    S2_text_rect = S2_text.get_rect(center=(S2_rect.right + 20, legend_height / 2 + 30))
    screen.blit(S2_text, S2_text_rect)

    S3_text = font.render('S3', True, black)
    S3_text_rect = S3_text.get_rect(center=(S3_rect.right + 20, legend_height / 2 + 30))
    screen.blit(S3_text, S3_text_rect)

    S4_text = font.render('S4', True, black)
    S4_text_rect = S4_text.get_rect(center=(S4_rect.right + 20, legend_height / 2 + 30))
    screen.blit(S4_text, S4_text_rect)

    starter_text = font.render('Starter', True, black)
    starter_text_rect = starter_text.get_rect(center=(starter.right + 30, legend_height / 2 + 30))
    screen.blit(starter_text, starter_text_rect)


def show_status(screen, width, height, legend_height):
    font = pygame.font.SysFont('Arial', 21)
    text = "Spread: "+str(len(people_exposed)) + " out of "  + str(len(total_people))
    text_rect = pygame.Rect(10, height - legend_height / 2 + 20, 25, 25)
    status_text = font.render(text, True, black)
    status_text_rect = status_text.get_rect(center=(text_rect.right + 100, legend_height / 2 + 570))
    status_text_rect.width += 6
    status_text_rect.height += 6
    screen.fill((255, 235, 255), rect=status_text_rect)
    screen.blit(status_text, status_text_rect)
    pygame.draw.rect(screen, (10, 10, 10), status_text_rect, 1)

    font = pygame.font.SysFont('Arial', 21)
    text = "Generation: " + str(len(percent_exposed))
    text_rect = pygame.Rect(20, height - legend_height / 2 + 20, 25, 25)
    status_text = font.render(text, True, black)
    status_text_rect = status_text.get_rect(center=(text_rect.right + 340, legend_height / 2 + 570))
    status_text_rect.width += 6
    status_text_rect.height += 6
    screen.fill((255, 235, 255), rect=status_text_rect)
    screen.blit(status_text, status_text_rect)
    pygame.draw.rect(screen, (10, 10, 10), status_text_rect, 1)



def show_status_last(screen, width, height, legend_height, text):
    font = pygame.font.SysFont('Arial', 15)
    text_rect = pygame.Rect(20, height - legend_height / 2 + 20, 20, 20)
    status_text = font.render(text, True, black)
    status_text_rect = status_text.get_rect(center=(text_rect.right + 200, legend_height / 2 + 600))



def main():
    # getting the user input for the simulation
    # window title
    title = "Spreading rumours Automaton simulation parameters"
    # informing the user which are the default params
    text = "Presented to you are the default parameters." + "\n" + "you can alter them if you want"
    # inputs fields
    inputs = ["Population density - P (0-1)",
              "The percentage of people who believe every rumor - S1 (0-100)",
              "The percentage of people whose basic probability they believe rumors is 2/3 - S2 (0-100)",
              "The percentage of people whose basic probability they believe rumors is 1/3 - S3 (0-100)",
              "The percentage of people who don't believe any rumor - S4 (0-100)",
              "The number of generations in which a rumor is not spread by a person who spread it - L (0-1000)",
              "Max number of generations"]
    # list of default params
    default_params = ["0.8", "45", "25", "10", "20", "8", "200"]
    output = multenterbox(text, title, inputs, default_params)

    if output == default_params:
        input_check(output)
        print("Default params are being used...")
    elif output == None:
        exit()
    else:
        flag = input_check(output)
        if flag is False:
            print("Wrong input!")
            exit()
        else:
            print("user parameters are being used")

    ####### initialize

    mat = np.full((mat_size, mat_size), None)
    mat = initialize(mat)
    # Initialize pygame
    legend_height = 90
    width = 500
    height = 500 + 60 + legend_height

    cell_length = width / mat_size
    # initialize game
    pygame.init()
    # create screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("simulation")
    # setting clock
    clock = pygame.time.Clock()

    starter = random.choice(total_people)
    rumor_spreaders = spread_rumor(mat, [starter])
    starter.set_num_generations()

    generation = 0
    # white color for the screen

    num_of_people = int(P * (mat_size * mat_size))

    game_running = True

    while game_running and generation <= max_generation and len(rumor_spreaders) and len(
            people_exposed) != num_of_people:
        generation += 1
        rumor_spreaders = spread_rumor(mat, rumor_spreaders)
        update_percentage()

        screen.fill(white)
        show_legend1(screen, width, legend_height)
        show_status(screen, width, height, legend_height)
        show_params(screen)

        for row in range(mat_size):
            for col in range(mat_size):
                # if there's someone in the cell
                # calc rec size for filling
                rect = (col * 5, row * 5 + legend_height, cell_length, cell_length)
                # check status and choose the right color
                if mat[row][col] is not None:
                    person = mat[row][col]
                    if person.num_generations != 0:
                        screen.fill((255, 0, 0), rect=rect)  # red
                        if person.num_generations == L:
                            screen.fill((255, 255, 60), rect=rect)
                    else:
                        screen.fill(black, rect=rect)  # black
                        if person.heard_rumor():
                            screen.fill((60, 60, 60), rect=rect)  # black

                else:
                    screen.fill(lightgrey, rect=rect)

        rect = (starter.column * 5, starter.row * 5 + legend_height, cell_length, cell_length)
        screen.fill((0, 0, 255), rect=rect)

        pygame.display.update()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False

        ###

    text = ""
    if generation > max_generation:
        print("max_generation stop!")
        text = "max_generation stop!"
    elif not len(rumor_spreaders):
        print("no more spreaders!")
        text = "no more spreaders!"
    elif len(people_exposed) == num_of_people:
        print("everybody heard!")
        text = "everybody heard!"

    print(len(total_people) - len(people_exposed), "people didn't heard out of", len(total_people))
    text += "    " + str(len(total_people) - len(people_exposed)) + " people didn't heard out of " + str(
        len(total_people))
    # last view
    while game_running:

        screen.fill(white)
        show_legend2(screen, width, legend_height)
        show_params(screen)
        for row in range(mat_size):
            for col in range(mat_size):
                # if there's someone in the cell
                # calc rec size for filling
                rect = (col * 5, row * 5 + legend_height, cell_length, cell_length)
                # check status and choose the right color
                if mat[row][col] is not None:
                    person = mat[row][col]
                    if person.base_doubt == 'S1':
                        screen.fill((255, 0, 0), rect=rect)
                        if person.heard_rumor():
                            screen.fill((155, 0, 0), rect=rect)
                    elif person.base_doubt == 'S2':
                        screen.fill((0, 255, 0), rect=rect)
                        if person.heard_rumor():
                            screen.fill((0, 155, 0), rect=rect)
                    elif person.base_doubt == 'S3':
                        screen.fill((0, 0, 255), rect=rect)
                        if person.heard_rumor():
                            screen.fill((0, 0, 155), rect=rect)
                    elif person.base_doubt == 'S4':
                        screen.fill((100, 100, 100), rect=rect)
                        if person.heard_rumor():
                            screen.fill((0, 0, 0), rect=rect)
                else:
                    screen.fill(lightgrey, rect=rect)
        rect = (starter.column * 5, starter.row * 5 + legend_height, cell_length, cell_length)
        screen.fill((205, 255, 255), rect=rect)
        ###
        show_status_last(screen, width, height, legend_height, text)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False

    plt.plot(percent_exposed)
    plt.xlabel('Generations')
    plt.ylabel('Percentage of people who heard rumor')
    plt.show()
    plt.plot(num_people_exposed)
    plt.xlabel('Generations')
    plt.ylabel('Number of people who heard rumor')
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
