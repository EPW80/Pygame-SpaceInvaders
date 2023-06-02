# Erik Williams
# CPSC 386-02
# 2023-04-20
# epwilliams@csu.fullerton.edu
# @EPW80
#
# Lab 05-00
#
# This is my Space Invaders project!
#

"""This is my Space Invaders project!"""

import pickle
import pygame
from player import Player

def from_file(pickle_file):
    """Read a pickled object from a file"""
    with open(pickle_file, "rb") as file_handle:
        players = pickle.load(file_handle)
    return players


def save_score_to_pickle(player_name, score):
    """Save score to a pickle file"""
    file_name = "scores.pkl"

    bullet_group = pygame.sprite.Group()
    new_player = Player(bullet_group, player_name, score)

    try:
        with open(file_name, "rb") as pickle_file:
            player_list = pickle.load(pickle_file)
    except (FileNotFoundError, EOFError):
        player_list = []

    player_list.append(new_player)

    with open(file_name, "wb") as pickle_file:
        pickle.dump(player_list, pickle_file, pickle.HIGHEST_PROTOCOL)
