import pygame
import random
import time

display_width = 900
display_height = 700

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
background = (102, 153, 153)
blue = (0, 102, 255)
grey = (128, 128, 128)

pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))

box_size = 27
board_space = 3
num_squares = 10
board_size = box_size * num_squares + (num_squares+1) * board_space
x_off = (display_width - board_size) / 2

name = "Battleship: Vengeance"
ships = [("Carrier", 5), ("Battleship", 4), ("Cruiser", 3), ("Submarine", 3), ("Destroyer", 2)]
filename = "123.txt"


class Box:
    def __init__(self, x, y, surface, y_off, ship=None, hit=False):
        self.x = x
        self.y = y
        self.ship = ship
        self.hit = hit
        self.surface = surface
        self.y_off = y_off
        self.x_pixel = x * box_size + (x+1) * board_space
        self.y_pixel = y * box_size + (y + 1) * board_space

        self.rect = pygame.Rect(self.x_pixel + x_off, self.y_pixel + self.y_off, box_size,  box_size)
        pygame.draw.rect(surface, blue, [self.x_pixel, self.y_pixel, box_size, box_size])

    def get_xy(self):
        return self.x, self.y

    def has_ship(self):
        if self.ship is None:
            return False
        else:
            return True

    def place_ship(self, ship):
        self.ship = ship

    def colour(self, colour):
        pygame.draw.rect(self.surface, colour, [self.x_pixel, self.y_pixel, box_size, box_size])
        gameDisplay.blit(self.surface, (x_off, self.y_off))
        pygame.display.update()


def generate_user():
    user_surface = pygame.Surface((board_size, board_size))
    user_surface.fill(black)
    y_off = user_surface.get_height() + 70
    user = [[Box(x, y, user_surface, y_off) for y in range(num_squares)] for x in range(num_squares)]
    gameDisplay.blit(user_surface, (x_off, y_off))
    return user


def generate_computer():
    y_off = 20
    computer_surface = pygame.Surface((board_size, board_size))
    computer_surface.fill(black)
    computer = [[Box(x, y, computer_surface, y_off) for y in range(num_squares)] for x in range(num_squares)]
    gameDisplay.blit(computer_surface, (x_off, y_off))
    return computer


def get_box_click(grid):
    good_click = False
    while not good_click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                for row in grid:
                    for box in row:
                        if box.rect.collidepoint(pos):
                            return box.get_xy()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


def check_valid(grid, x, y, direction, ship):
    valid = True
    boxes = []
    if direction == pygame.K_LEFT:
        for i in range(ship[1]):
            try:
                if grid[x-i][y].has_ship() or x - i < 0:
                    valid = False
                else:
                    boxes.append(grid[x-i][y])
            except IndexError:
                valid = False

    elif direction == pygame.K_RIGHT:
        for i in range(ship[1]):
            try:
                if grid[x + i][y].has_ship():
                    valid = False
                else:
                    boxes.append(grid[x + i][y])
            except IndexError:
                valid = False

    elif direction == pygame.K_UP:
        for i in range(ship[1]):
            try:
                if grid[x][y - i].has_ship() or y - i < 0:
                    valid = False
                else:
                    boxes.append(grid[x][y - i])
            except IndexError:
                valid = False

    elif direction == pygame.K_DOWN:
        for i in range(ship[1]):
            try:
                if grid[x][y + i].has_ship():
                    valid = False
                else:
                    boxes.append(grid[x][y + i])
            except IndexError:
                valid = False

    return valid, boxes


def user_fill(grid, panel):

    previous_boxes = []

    panel.display("Place your ships")
    panel.display("from largest to smallest.")
    panel.display("Click to select a tile,")
    panel.display("use the arrow keys for")
    panel.display("direction, then press")
    panel.display("enter to confirm each ship.")
    panel.display("")

    for ship in ships:

        ship_x, ship_y = get_box_click(grid)

        has__direction = False
        confirmed = False
        while not has__direction or not confirmed:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                            event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        for box in previous_boxes:
                            box.place_ship(None)
                        direction = event.key
                        valid, boxes = check_valid(grid, ship_x, ship_y, direction, ship)
                        if not valid:
                            for box in previous_boxes:
                                box.place_ship(ship[0])
                        if valid:
                            for box in previous_boxes:
                                box.place_ship(None)
                                box.colour(blue)
                            has__direction = True
                            previous_boxes = boxes
                            for box in boxes:
                                box.place_ship(ship[0])
                                box.colour(grey)
                    elif event.key == pygame.K_RETURN and has__direction:
                        previous_boxes = []
                        confirmed = True

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for row in grid:
                        for box in row:
                            if box.rect.collidepoint(pos):
                                ship_x, ship_y = box.get_xy()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


def computer_fill(grid):

    boxes = []

    for ship in ships:
        valid = False
        while not valid:
            ship_x = random.randint(0, 9)
            ship_y = random.randint(0, 9)
            directions = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
            valid, boxes = check_valid(grid, ship_x, ship_y, random.choice(directions), ship)

        for box in boxes:
            box.place_ship(ship[0])


def user_move(grid, hits, info_panel, ship_panel):
    x, y = get_box_click(grid)
    valid = False
    while not valid:
        good_guess, hit = hit_box(grid, x, y, info_panel, ship_panel)
        if good_guess and hit:
            return hits+1
        elif good_guess:
            return hits
        else:
            x, y = get_box_click(grid)


def hit_box(grid, x, y, info_panel, ship_panel):
    if grid[x][y].has_ship() and not grid[x][y].hit:
        grid[x][y].colour(red)
        grid[x][y].hit = True
        info_panel.display("Hit!")
        ship_panel.hit_ship(grid[x][y].ship)
        ship_panel.display_ships()
        return True, True
    elif not grid[x][y].hit:
        grid[x][y].colour(white)
        grid[x][y].hit = True
        info_panel.display("Miss")
        return True, False
    else:
        return False, False


def computer_move(grid, hits, info_panel, ship_panel):
    if hits > 0:
        for i in range(10):
            for j in range(10):
                if grid[i][j].hit and grid[i][j].has_ship():
                    try:
                        good_guess, hit = hit_box(grid, i+1, j, info_panel, ship_panel)
                        if good_guess and hit:
                            return hits + 1
                        elif good_guess:
                            return hits
                    except IndexError:
                        pass
                    try:
                        good_guess, hit = hit_box(grid, i-1, j, info_panel, ship_panel)
                        if good_guess and hit:
                            return hits + 1
                        elif good_guess:
                            return hits
                    except IndexError:
                        pass
                    try:
                        good_guess, hit = hit_box(grid, i, j+1, info_panel, ship_panel)
                        if good_guess and hit:
                            return hits + 1
                        elif good_guess:
                            return hits
                    except IndexError:
                        pass
                    try:
                        good_guess, hit = hit_box(grid, i, j-1, info_panel, ship_panel)
                        if good_guess and hit:
                            return hits + 1
                        elif good_guess:
                            return hits
                    except IndexError:
                        pass
    x, y = random.randint(0, 9), random.randint(0, 9)
    valid = False
    while not valid:
        good_guess, hit = hit_box(grid, x, y, info_panel, ship_panel)
        if good_guess and hit:
            return hits + 1
        elif good_guess:
            return hits
        else:
            x, y = random.randint(0, 9), random.randint(0, 9)


def check_win(hits):
    if hits == 17:
        return True
    else:
        return False


def insertion_sort(names, scores):      # insertion sort

    for i in range(1, len(scores)):   # insertion sort algorithm
        temp_val = scores[i]
        temp_name = names[i]
        j = i-1
        while temp_val > scores[j] and j >= 0:
            scores[j+1], names[j+1] = scores[j], names[j]    # swaps the data
            j -= 1
        scores[j+1], names[j+1] = temp_val, temp_name        # swaps vales

    return names, scores


def write_file(user_name, score):   # writes an array to the file
    found = False
    try:
        names, scores = read_file()
    except FileNotFoundError:
        names, scores = [], []
    file = open(filename, "w")
    for i in range(len(names)):
        if names[i] == user_name:
            scores[i] += score
            found = True
    if not found:
        names.append(user_name)
        scores.append(score)
    for i in range(len(names)):
        file.write(names[i] + " " + str(scores[i]) + "\n")
    file.close()


def read_file():
    file = open(filename, "r")
    names = []
    scores = []
    for line in file:  # separates the stats into names and scores
        names.append(line.split(" ")[0].strip())
        scores.append(int(line.split(" ")[1].strip()))
    file.close()
    return insertion_sort(names, scores)


def show_text(text, font, size, colour, surface, position, center):
    my_font = pygame.font.SysFont(font, size)
    message = my_font.render(text, False, colour)
    if center:
        message_rect = message.get_rect(center=position)
        surface.blit(message, message_rect)
    else:
        surface.blit(message, position)

    pygame.display.update()


class Button:
    def __init__(self, x, y, surface, colour, text):
        self.surface = surface
        self.x = x
        self.y = y
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, 180, 80)
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(self.surface, colour, self.rect)
        show_text(self.text, "Arial", 40, black, self.surface, (self.x, self.y), True)

    def colour(self, colour):
        pygame.draw.rect(self.surface, colour, self.rect)
        show_text(self.text, "Arial", 40, black, self.surface, (self.x, self.y), True)


class InstructionPanel:
    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.surface = surface
        self.counter = 0
        self.rect = pygame.Rect(self.x, self.y, 250, 450)

    def colour(self, colour):
        pygame.draw.rect(self.surface, colour, self.rect)

    def display(self, text):
        if self.counter > 8:
            self.counter = 0
            self.colour(background)
        show_text(text, "Arial", 20, black, self.surface, (self.x, self.y + self.counter*25), False)
        self.counter += 1


class ShipPanel:
    def __init__(self, x, y, surface):
        self.x = x
        self.y = y
        self.surface = surface
        self.counter = 0
        self.rect = pygame.Rect(self.x, self.y, 250, 450)
        self.healths = [5, 4, 3, 3, 2]

    def colour(self, colour):
        pygame.draw.rect(self.surface, colour, self.rect)

    def hit_ship(self, ship_hit):
        for i in range(len(ships)):
            if ship_hit == ships[i][0]:
                self.healths[i] -= 1

    def display_ships(self):
        for i in range(len(ships)):
            if self.healths[i] > 0:
                show_text(ships[i][0], "Arial", 20, black, self.surface, (self.x, self.y + self.counter*25), False)
            else:
                show_text(ships[i][0], "Arial", 20, red, self.surface, (self.x, self.y + self.counter*25), False)
            self.counter += 1
        self.counter = 0

    def num_sunk(self):
        sunk = 0
        for health in self.healths:
            if health == 0:
                sunk += 1
        return sunk

    def is_sunk(self, ship):
        for i in range(len(ships)):
            if ship == ships[i][0]:
                if self.healths[i] > 0:
                    return False
                else:
                    return True


def game_ending(text, score, user_name):
    gameDisplay.fill(background)
    x = display_width / 2
    y = display_height / 2
    show_text(text, "Arial", 50, black, gameDisplay, (x, y - 150), True)
    show_text("Score: "+str(score), "Arial", 50, black, gameDisplay, (x, y - 70), True)
    again = Button(x, y + 50, gameDisplay, blue, "Play Again")
    log_out = Button(x, y + 150, gameDisplay, blue, "Log out")
    exit_game = Button(x, y + 250, gameDisplay, blue, "Exit")
    write_file(user_name, score)

    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos_x, pos_y = pygame.mouse.get_pos()
                if again.rect.collidepoint(pos_x, pos_y):
                    game_loop(user_name)
                elif exit_game.rect.collidepoint(pos_x, pos_y):
                    pygame.quit()
                    quit()
                elif log_out.rect.collidepoint(pos_x, pos_y):
                    game_start()

        pos_x, pos_y = pygame.mouse.get_pos()
        if again.rect.collidepoint(pos_x, pos_y):
            again.colour(red)
        elif exit_game.rect.collidepoint(pos_x, pos_y):
            exit_game.colour(red)
        elif log_out.rect.collidepoint(pos_x, pos_y):
            log_out.colour(red)
        else:
            again.colour(blue)
            exit_game.colour(blue)
            log_out.colour(blue)


def game_loop(user_name):

    gameDisplay.fill(background)
    pygame.display.set_caption(name)
    pygame.draw.line(gameDisplay, black, (0, display_height / 2), (display_width, display_height / 2), 3)

    x = 650
    y = 100
    show_text("Leaderboard", "Arial", 30, black, gameDisplay, (x, y-50), False)
    try:
        names, scores = read_file()
        for i in range(len(names)):
            size = len(names[i])
            for j in range(12-size):
                names[i] += " "
        length = 5 if (len(names) > 4) else len(names)
        for i in range(length):
            print(str(i+1)+". "+names[i]+" "+str(scores[i]))
            show_text(str(i+1)+". "+names[i]+" "+str(scores[i]), "Arial", 25, black, gameDisplay, (x, y+i*30), False)
    except FileNotFoundError:
        pass

    info_panel = InstructionPanel(x, display_height / 2 + 50, gameDisplay)
    info_panel.display("Welcome to")
    info_panel.display("Battleship: Vengeance!")

    user_ships = ShipPanel(50, display_height / 2 + 50, gameDisplay)
    user_ships.display_ships()
    computer_ships = ShipPanel(50, 50, gameDisplay)
    computer_ships.display_ships()

    user_grid = generate_user()
    computer_grid = generate_computer()
    pygame.display.update()

    user_fill(user_grid, info_panel)
    computer_fill(computer_grid)

    info_panel.display("Fire away!")
    info_panel.display("Use the mouse to select")
    info_panel.display("boxes in the top grid.")

    user_hits = 0
    computer_hits = 0
    start = time.time()

    game_exit = False

    while not game_exit:
        for user_event in pygame.event.get():
            if user_event.type == pygame.QUIT:
                game_exit = True
                pygame.quit()
                quit()

        user_hits = user_move(computer_grid, user_hits, info_panel, computer_ships)
        if check_win(user_hits):
            info_panel.display("You Win!")
            end = time.time()
            score = 2000 - int((end-start)*20) + 50 * computer_ships.num_sunk()
            if score < 100:
                score = 100
            time.sleep(3)
            game_ending("You win! All enemy ships have been sunk.", score, user_name)
        else:
            computer_hits = computer_move(user_grid, computer_hits, info_panel, user_ships)
            if check_win(computer_hits):
                info_panel.display("You Lose!")
                score = 50 * computer_ships.num_sunk()
                time.sleep(3)
                game_ending("You lost! All friendly ships have been sunk.", score, user_name)


def game_start():
    gameDisplay.fill(background)
    x = display_width / 2
    y = display_height / 2
    show_text(name, "Arial", 50, black, gameDisplay, (x, y - 250), True)
    show_text("By: James Bundgard", "Arial", 40, black, gameDisplay, (x, y - 170), True)
    text_input = Button(x, y - 50, gameDisplay, grey, "")
    show_text("Enter a username less than 11 characters into the box above to play.",
              "Arial", 20, black, gameDisplay, (x, y + 40), True)
    user_name = ""
    start_game = Button(x, y + 150, gameDisplay, blue, "Start")
    exit_game = Button(x, y + 250, gameDisplay, blue, "Exit")

    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos_x, pos_y = pygame.mouse.get_pos()
                if start_game.rect.collidepoint(pos_x, pos_y) and 0 < len(user_name) < 12:
                    game_loop(user_name)
                elif exit_game.rect.collidepoint(pos_x, pos_y):
                    pygame.quit()
                    quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                elif event.key == pygame.K_RETURN and 0 < len(user_name) < 12:
                    game_loop(user_name)
                else:
                    if event.unicode.isalnum() and len(user_name) < 10:
                        user_name += event.unicode
                text_input.colour(grey)
                show_text(user_name, "Arial", 30, black, gameDisplay, (x, y - 50), True)

        pos_x, pos_y = pygame.mouse.get_pos()
        if start_game.rect.collidepoint(pos_x, pos_y):
            start_game.colour(red)
        elif exit_game.rect.collidepoint(pos_x, pos_y):
            exit_game.colour(red)
        else:
            start_game.colour(blue)
            exit_game.colour(blue)


game_start()
