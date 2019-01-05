MAX_PLAYER_LVL = 100
MAX_GAME_SIZE = 100  # in number of players
MAX_GAME_TIME = 100  # in minutes

SCALING_BONUS_BASE = 0.75
SCALING_BONUS_MOD = 0.25

PLACE_FINISHED_BASE = 51
PLACE_FINISHED_MULT = 2

DOWNED_MULT = -10

KILLS_MULT = 5
KILLS_MOD = 5

ASSISTS_MULT = 5
ASSISTS_MOD = 5
ASSISTS_DIV = 2

DEATH_PENALTY = -75

ACCURACY_BASE = 0.95
ACCURACY_MULT = 0.1

VICTORY_BONUS = 100

STAYED_BONUS = 25

LOSS_BASE = 1
LOSS_MULT = 0.04

TIME_SURV_BASE = 0.5


def get_elo_change_scores(average_lvl, player_lvl, place_finished, kills, downs, assists, accuracy, time_survived,
                          game_length):
    """Function to calculate ELO change of a player with given game stats.

    Args:
        player_lvl: Level of player who's elo change is being calculated.

        average_level: Average level of players in match.

        place_finished: Place the player finished

        kills: Number of kills the player had.

        downs: Number of times the player was "downed" and had to be revived.

        assists: Number of assists the player had.

        accuracy: Percentage of shots hit.

        time_survived: Time in minutes the player was a live in the game.

    Returns:
        Dict of floats of the elo adjustments that would be made depending on if the player: lost, won,
        died and continued to spectate while team won, died and left the game while team won.

    """
    elo_change = {'lost': (), 'won_stayed': (), 'won_left': (), 'won_lived': ()}

    place_s = calc_place_score(place_finished)
    down_s = calc_down_score(downs)
    kill_s = calc_kill_score(kills)
    assist_s = calc_assist_score(assists)
    accuracy_s = calc_accuracy_score(accuracy)
    loss_mult = calc_loss_mult(average_lvl, player_lvl)
    time_mult = calc_time_survived_mult(time_survived, game_length)

    scaling_bonus = calc_scale_bonus(average_lvl, player_lvl)

    elo_change['lost'] = calc_elo(place_s, down_s, kill_s, assist_s, accuracy_s, loss_mult, time_mult, scaling_bonus,
                                  False, True, False)

    elo_change['won_stayed'] = calc_elo(place_s, down_s, kill_s, assist_s, accuracy_s, loss_mult, time_mult,
                                        scaling_bonus, True, True, True)

    elo_change['won_left'] = calc_elo(place_s, down_s, kill_s, assist_s, accuracy_s, loss_mult, time_mult,
                                      scaling_bonus, True, True, False)

    elo_change['won_lived'] = calc_elo(place_s, down_s, kill_s, assist_s, accuracy_s, loss_mult, time_mult,
                                       scaling_bonus, True, False, True)

    return elo_change


def calc_kill_score(kills):
    """Calculates the 'Kill Score' based on a given number of kills

    Args:
        kills: Number of kills.

    Globals:
        KILLS_MULT: Global kills multiplier value.
        KILLS_MOD: Global kills modifier value.

    Returns:
        Int: Calculated 'Kill Score'.
    """
    return ((kills * KILLS_MULT) + KILLS_MOD) * kills


def calc_down_score(downs):
    """Calculates the 'Downed Score' based on a given number of times the player was downed.

    Args:
        downs: Number of times the player was downed in a game.

    Globals:
        DOWNED_MULT: Global downed multiplier.
    
    Returns:
        Int: Calculated 'Downed Score'
    """
    return downs * DOWNED_MULT


def calc_place_score(place_finished):
    """Calculates the 'Place Score' based on a given place.

    Args:
        place_finished: The place a player finished in a match.

    Globals: 
        PLACE_FINISHED_BASE: Global for the base score of the 'Place Score'.

    Returns:
        Int: Calculated 'Place score'.
    """
    return (PLACE_FINISHED_BASE - place_finished) * 2


def calc_assist_score(assists):
    """Calculates the 'Assist Score' based off a given number of asssits.

    Args:
        assists: Number of assists a player had.

    Globals:
        ASSISTS_MULT: Global assists multiplier.
        ASSISTS_MOD: Global modifier for the 'Assist Score'.

    Returns:
        Int: Calculated 'Assist Score'.
    """
    return (((assists * ASSISTS_MULT) + ASSISTS_MOD) * assists) / ASSISTS_DIV


def calc_accuracy_score(accuracy_percentage):
    """Calculates the 'Accuracy Score' based off of a given % accuracy.

    Args:
        accuracy_percentage: % accuracy of a player for a given game.

    Globals:
        ACCURACY_BASE: Global for the base value of the 'Accuracy Score'.
        ACCURACY_MULT: Global for the multiplier used in the 'Accuracy Score'.
        
    Returns:
        Float: Calculated Accuracy score between 0 and 1
    """
    return ACCURACY_BASE + (accuracy_percentage * ACCURACY_MULT)


def calc_loss_mult(average_lvl, player_lvl):
    """Calculates the loss multiplier for a given player.

    Args:
        average_lvl: Average level of players in a given game.
        player_lvl: Player level.

    Globals:
        LOSS_BASE: Base value of loss multiplier.
        LOSS_MULT: Multiplier value used to calculate loss multiplier
    
    Returns:
        Float: Calculated loss multiplier for a given player and game.
    """
    return LOSS_BASE + (LOSS_MULT * (player_lvl / average_lvl))


def calc_time_survived_mult(time_survived, game_length):
    """Calculates the time survived multiplier for a player for a given game.

    Args:
        time_survived: The time the player survived in minutes.
        game_length: The length of the game in minutes.

    Globals:
        TIME_SURV_BASE: Base score for time multiplier value.

    Returns:
        Float: Calcualted time survived multiplier value.
    """
    return TIME_SURV_BASE + (time_survived / game_length)


def calc_elo(place_s, down_s, kill_s, assist_s, accuracy_s, loss_mult, time_mult, scaling_bonus, won, died, stayed):
    """Calcualtes the elo gained or lossed for a player based on scores of a single game.

    Args:
        place_s: Place score for given game.
        down_s: Downed score for a given game.
        kill_s: Kill score for a given game.
        assist_s: Assist score for a given game.
        accuracy_s: Accuracy score for a given game.
        loss_mult: Loss multiplier for a given game.
        time_mult: Time multiplier for a given game.
        scaling_bonus: Scaling bonus achieved for a given game.
        won: bool, true if the player won the game.
        died: bool, true if player died in the game
        stayed: bool, true if the player stayed till the end of the game.

    Globals:
        DEATH_PENALTY: Global of the elo penalty for dying.
        STAYED_BONUS: Global of the elo bonus for staying till the end of the game.
    """
    death_penalty = DEATH_PENALTY if died else 0
    stayed_bonus = STAYED_BONUS if stayed else -STAYED_BONUS

    score = 0
    score_with_bonus = 0

    if won:
        score = (((kill_s + assist_s) * accuracy_s) * time_mult) + (
            death_penalty + down_s + stayed_bonus + VICTORY_BONUS + place_s)
        score_with_bonus = (((kill_s + assist_s) * accuracy_s) * time_mult) + (
            death_penalty + down_s + stayed_bonus + place_s) + (VICTORY_BONUS * scaling_bonus)
    else:
        score = (((kill_s + assist_s) * accuracy_s) * time_mult) + place_s + (loss_mult * (down_s + DEATH_PENALTY))
        score_with_bonus = score

    return (score, score_with_bonus)


def calc_scale_bonus(average_lvl, player_lvl):
    """Calcualtes the scale bonus of a player for a given game.

    Args:
        average_lvl: Average level of all players in a given game.
        player_lvl: Level of player the scale bonus is being calculated for.

    Globals:
        SCALING_BONUS_BASE: Global for base bonus value.
        SCALING_BONUS_MOD: Global modifier for bonus value.
    """
    return SCALING_BONUS_BASE + (SCALING_BONUS_MOD * (average_lvl / player_lvl))
