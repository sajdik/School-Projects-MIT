import ast
import sys
user_items_path = "../australian_users_items.json"
user_items_destination = "dataset/dataset.csv"

games_path = "../steam_games.json"
game_destination = "dataset/games.csv"

def load_file(file_path):
    data = []
    with open(file_path) as file:
        for line in file:
            data.append(ast.literal_eval(line))
    return data

def get_all_unique(data, id_str):
    seen = []
    for d in data:
        try:
            p = d[id_str]
        except:
            p = []
        if p not in seen:
            seen.append(p)

    return seen

# Creates file with game metadata
# Returns list of all used ids
def transform_games(source_path, destination_path):
    data = load_file(source_path)
    gameIds = {}
    publishers = get_all_unique(data,'publisher')
    genres = get_all_unique(data,'genres')
    genres = list({x for l in genres for x in l})
    specs = get_all_unique(data,'specs')
    specs = list({x for l in specs for x in l})
    game_publishers = []
    prices = []

    for game in data:
        try:
            publisher_name = game['publisher']
        except:
            publisher_name = 'None'
        try:
            price = str(game['price'])
            if not price.replace('.','').isnumeric():
                price = '0'
        except:
            price = '0'
        pid = publishers.index(publisher_name)
        prices.append(price)
        game_publishers.append(pid)

    with open(destination_path, "w") as f:
        f.write('\"game_id\",\"publisher\",\"price\"')
        
        for genre in genres:
            f.write(','+ genre)
        for spec in specs:
            f.write(','+ spec)
        f.write('\n')

        for i in range(len(data)):
            try:
                f.write(str(i) + ',' + str(game_publishers[i]) + ',' + prices[i])
                gameIds[data[i]['id']] = i
            except:
                print("Dont have id: ", data[i], file=sys.stderr)
            
            try:
                my_genres = data[i]['genres']
            except:
                my_genres = []

            try:
                my_specs = data[i]['specs']
            except:
                my_specs = []

            for genre in genres:
                if genre in my_genres:
                    f.write(',1')
                else:
                    f.write(',0')
            
            for spec in specs:
                if spec in my_specs:
                    f.write(',1')
                else:
                    f.write(',0')
            f.write('\n')

    return gameIds

# Create user-item file
def transform_user_items(source_path, destination_path, gameIds):
    data = load_file(source_path)
    with open(destination_path, "w") as f:
        f.write('\"user_id\",\"game_id\",\"playtime_forever\",\"playtime_2weeks\"\n')
        i = 0
        for user in data:
            if user['items_count'] > 5:
                
                for item in user['items']:
                    try:
                        f.write(str(i) + "," + str(gameIds[item['item_id']]) + "," + str(item['playtime_forever']) + "," + str(item['playtime_2weeks'])+'\n')
                    except:
                        pass
                        # print(user)
                i+=1
                    

gameIds = transform_games(games_path, game_destination)
transform_user_items(user_items_path, user_items_destination, gameIds)