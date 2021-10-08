def file_write(filename, dictionary):
    string = ""
    for key in dictionary:
        string += key + " = " + str(dictionary[key]) + "\n"
    file = open(filename + ".txt", "w")
    file.write(string)


def array_file_write(filename, dictionary):
    string = ""
    for key in dictionary:
        string += key + " ="
        for index in dictionary[key]:
            string += " " + str(index)
        string += "\n"
    file = open(filename + ".txt", "w")
    file.write(string)


def file_load(filename, dictionary):
    file = open(filename + ".txt", "r")
    for line in file:
        stat = line.split()
        dictionary[stat[0]] = int(stat[2])
    return dictionary


def array_file_load(filename, dictionary):
    file = open(filename + ".txt", "r")
    for line in file:
        stat = line.split()
        for index in range(3):
            dictionary[stat[0]][index] = int(stat[2 + index])
    return dictionary


def add_to_stats(stats, stat, value):
    for key in stats:
        if stat == key:
            stats[key] += value
    return stats


def add_to_upgrades(upgrades, upgrade, value):
    for key in upgrades:
        if upgrade == key:
            upgrades[key][0] += value
    return upgrades


def save_stats(filename, stats, coins, distance, enemies):
    stats = add_to_stats(stats, "coins", coins)
    stats = add_to_stats(stats, "distance_travelled", distance)
    stats = add_to_stats(stats, "enemies_killed", enemies)
    file_write(filename, stats)
    return stats


def save_upgrades(filename, upgrades, damage, health, jumps):
    upgrades = add_to_upgrades(upgrades, "extra_damage", damage)
    upgrades = add_to_upgrades(upgrades, "extra_health", health)
    upgrades = add_to_upgrades(upgrades, "extra_jumps", jumps)
    array_file_write(filename, upgrades)
    return upgrades
