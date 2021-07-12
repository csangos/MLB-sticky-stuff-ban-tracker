import statsapi

# 141, Toronto
# 144, Atlanta
# 113, Cincinnati
# 118, Kansas City
# 142, Minnesota
# 134, Pittsburgh
# 139, Tampa Bay
# 112, Chi Cubs
# 116, Detroit
# 146, Miami
# 120, Nats
# 121, Mets

# Game type:
# S: Spring Training
# R: Regular Season


# print (statsapi.lookup_team('MIA'))


def runs_query(start, end):
    return statsapi.schedule(start_date=start, end_date=end)


def get_runs():

    data = runs_query("04/01/2021", "06/20/2021")

    total_runs = 0
    game_count = 0
    game_ids = []

    for game in data:
        if game['status'] == "Final" and game['game_type'] == "R" and game['game_id'] not in game_ids:
            game_ids.append(game['game_id'])
            game_count += 1
            away_score = int(game['summary'].split("(")[1].split(")")[0])
            home_score = int(game['summary'].split("(")[2].split(")")[0])
            total_runs = total_runs + away_score + home_score

    post_data = runs_query("06/21/2021", "12/31/2021")

    post_total_runs = 0
    post_game_count = 0
    post_game_ids = []

    for game in post_data:
        if game['status'] == "Final" and game['game_type'] == "R" and game['game_id'] not in post_game_ids:
            post_game_ids.append(game['game_id'])
            post_game_count += 1
            post_away_score = int(game['summary'].split("(")[1].split(")")[0])
            post_home_score = int(game['summary'].split("(")[2].split(")")[0])
            post_total_runs = post_total_runs + post_away_score + post_home_score
            # print(game['summary'])

    before_avg = total_runs / game_count
    post_avg = post_total_runs / post_game_count

    print("\nBefore sticky stuff ban")
    print(f"Total games: {game_count}")
    print(f"Total runs: {total_runs}")
    print(f"Average runs per game: {before_avg:.2f}\n")

    print("After sticky stuff ban")
    print(f"Total games: {post_game_count}")
    print(f"Total runs: {post_total_runs}")
    print(f"Average runs per game: {post_avg:.2f}\n")

    print(f"Difference to date: {post_avg - before_avg:.2f}")


def get_hits():
    games_with_hits = runs_query("04/01/2021", "06/20/2021")
    game_count = 0
    game_ids = []
    hits = 0
    print("\nSumming pre sticky stuff total hits")
    for game in games_with_hits:
        if game['status'] == "Final" and game['game_type'] == "R" and game['game_id'] not in game_ids:
            game_ids.append(game['game_id'])
            game_count += 1
            if game_count % 50 == 0:
                print(game_count)
            box_score_details = statsapi.boxscore_data(gamePk=game['game_id'])
            hits = hits + box_score_details['away']['teamStats']['batting']['hits'] + \
                box_score_details['away']['teamStats']['batting']['hits']

    print("\nBefore sticky stuff ban")
    print(f"Total number of games: {game_count}")
    print(f"Total number of hits: {hits}")
    print(f"Hits per game: {hits / game_count:.2f}")

    post_games_with_hits = runs_query("06/21/2021", "12/31/2021")
    post_game_count = 0
    post_hits = 0
    post_game_ids = []
    print("\nSumming post sticky stuff total hits")

    for game in post_games_with_hits:
        if game['status'] == "Final" and game['game_type'] == "R" and game['game_id'] not in post_game_ids:
            post_game_ids.append(game['game_id'])
            post_game_count += 1
            if post_game_count % 50 == 0:
                print(post_game_count)
            box_score_details = statsapi.boxscore_data(gamePk=game['game_id'])
            post_hits = post_hits + box_score_details['away']['teamStats']['batting']['hits'] + \
                box_score_details['away']['teamStats']['batting']['hits']

    print("\nBefore sticky stuff ban")
    print(f"Total number of games: {post_game_count}")
    print(f"Total number of hits: {post_hits}")
    print(f"Hits per game: {post_hits / post_game_count:.2f}")


def get_hits_v2():
    #  hits_avg = 0
    #  games_with_hits = runs_query("04/01/2021", "06/20/2021")
    #  game_count = 0
    #  game_ids = []
    #  hits = 0

    #  print(
    #      f"\nSumming pre sticky stuff total hits...")
    #  for game in games_with_hits:
    #      if game['status'] == "Final" and game['game_type'] == "R" and game['game_id'] not in game_ids:
    #          game_ids.append(game['game_id'])
    #          game_count += 1
    #          if game_count % 50 == 0:
    #              print(f"{game_count} / {hits}")
    #          boxscore_lines = statsapi.linescore(game['game_id']).splitlines()
    #          hits += int(boxscore_lines[1].split()[-2]) + \
    #              int(boxscore_lines[2].split()[-2])

    #  print("\nBefore sticky stuff ban")
    #  print(f"Total number of games: {game_count}")
    #  print(f"Total number of hits: {hits}")
    #  hits_avg = hits / game_count
    #  print(f"Hits per game: {hits / game_count:.2f}")

    #
    # Post Ban
    #
    pre_hits = 16826
    pre_games = 1064
    pre_hits_avg = pre_hits/pre_games

    post_games_with_hits = runs_query("06/21/2021", "12/31/2021")
    post_game_count = 0
    post_game_ids = []
    post_hits = 0

    print(
        f"\nSumming post sticky stuff total hits...")
    for game in post_games_with_hits:
        if game['status'] == "Final" and game['game_type'] == "R" and game['game_id'] not in post_game_ids:
            post_game_ids.append(game['game_id'])
            post_game_count += 1
            if post_game_count % 50 == 0:
                print(f"{post_game_count} / {post_hits}")
            boxscore_lines = statsapi.linescore(
                game['game_id']).splitlines()
            # print(boxscore_lines)
            post_hits += int(boxscore_lines[1].split()[-2]) + \
                int(boxscore_lines[2].split()[-2])

    print("\nAfter sticky stuff ban")
    print(f"Total number of games: {post_game_count}")
    print(f"Total number of hits: {post_hits}")
    post_hits_avg = post_hits / post_game_count
    print(f"Hits per game: {post_hits_avg:.2f}")
    print(f"Delta: {post_hits_avg - pre_hits_avg:.2f}")


# get_runs()
# get_hits()
get_hits_v2()
