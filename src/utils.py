
def try_all_neighbours(field_size, atoms):
    move = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    for x in range(field_size):  # try all neighbours
        for y in range(field_size):
            for dx, dy in move:
                current_x = x + dx
                current_y = y + dy
                if 0 <= current_x < field_size and 0 <= current_y < field_size:
                    atoms[x][y].add_neighbour(atoms[current_x][current_y])  # add neighbour to atom