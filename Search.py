from lookForwardBackward import lookForwardBackward

'''This program helps the user explore a data set of
over a thousand video games released between
2004 and 2008.

Siana Lai
November 10th, 2025
'''

def main():
    menu()
    games = game_list('video_games.csv', ",")
    while True: 
        choice = user_choice()

        if choice == 1:
            while True:
                year = input("Enter a year")
                if year.isdigit():
                    if int(year) >= 2004 and int(year) <= 2008:
                        break
                    else:
                        print("Please try again, year must be between 2004 and 2008")
                else: 
                    print("Please try again, enter a year between 2004 and 2008")
            console = input("Enter a console:")
            results = year_search(games, year, console)
            display(results)

        elif choice == 2:
            title = input("Enter a title:")
            first_index = title_search(games, title)

            if first_index == -1:
                print("no results found")
                continue

            back_matches = lookForwardBackward(games, first_index, title, -1)
            front_matches = lookForwardBackward(games, first_index, title, 1)
            results = ([games[first_index]] + front_matches + back_matches)[:25]
            display(results)

        elif choice == 3:
            console = input("Enter a console:")
            genre = input("Enter a genre:")
            results = console_genre(games, console, genre)

            if results == -1:
                print("no results found")
                continue

            display(results[:25])
        
        elif choice == 4:
            while True:
                year = input("Enter a year")
                if year.isdigit():
                    if int(year) >= 2004 and int(year) <= 2008:
                        break
                    else:
                        print("Please try again, year must be between 2004 and 2008")
                else: 
                    print("Please try again, enter a year between 2004 and 2008")
            results = games_by_sales(games, year)

            if results == -1:
                print("no results found")
                continue
            
            display(results[:25])
        
        elif choice == 5:
            genre_list = genre_search(games)
            print('List of game genres in the data set:')
            print("-"*40)
            for genre in genre_list:
                print(genre)

        elif choice == 6:
            print("Goodbye!")
            break

def menu():
    '''gives the user the menu options: search by game title, search by console/ year or quit. Only allows valid inputs.
    Then asks them to input their choice. Returns the 
    user input.'''
    print('''
This program helps the user explore a data set of
over a thousand video games released between
2004 and 2008.
          
In particular , you can :
1. Search by console and release year
2. Search by game title
3. Rank best reviewed games by console and genre
4. Find top selling games by year
5. Help : list possible Genres
6. Quit''')

def user_choice():
    while True:
        user_input = input("Choice:")
        if user_input in ['1', '2', '3', '4', '5', '6']:
            return int(user_input)
        else:
            print("Invalid choice, please try again:")
        
def game_list(filename: str, delimiter: str): 
    '''this function takes the video_games list and converts it into
    a list of lists. Each feature is stored with its correct type.'''
    game_list = []
    with open(filename, 'r') as source:
        next(source)
        for line in source:
            row = line.strip().split(delimiter)
            for i in [1, 3, 8,]:
                if len(row) > i:
                    row[i] = int(row[i])
            for i in [4, 5, 9]:
                if len(row) > i:
                    row[i] = float(row[i])
            game_list.append(row)
    return game_list

def title_search(games, title) -> int:
    """Finds title inputted by user within the list of games.
    Returns: index of item if found, otherwise -1
    """
    low = 0
    high = len(games) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_title = games[mid][0]

        if mid_title.lower().startswith(title.lower()):  # we found it
            return mid
        elif title.lower() < mid_title.lower():  # update high
            high = mid - 1
        else:  # update low
            low = mid + 1

    return -1  # item is not found

def year_search(games, year, console) -> list[list[str]]: 
    '''Returns a list of games that match the year and console entered by user'''
    year = int(year)
    lines = []
    for line in games:
        if line[8] == year and line[6].lower() == console.lower():
            lines.append(line)
    if lines:
        return lines
    else:
        return -1

def console_genre(games, console, genre) -> list[list[str]]:
    '''get a list of games filtered by Console and Genre and 
    sorted by review score from highest to lowest'''
    lines = []
    for line in games:
        console_match = (console.lower() == "any" or line[6].lower() == console.lower())
        genre_match = (genre.lower() == "any" or genre.lower() in line[2].lower())

        if console_match and genre_match:
            lines.append(line)

    if not lines: 
        return -1

    n = len(lines)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if lines[j][3] < lines[min_index][3]:
                min_index = j
        lines[i], lines[min_index] = lines[min_index], lines[i]
    lines.reverse()
    return lines

def genre_search(games) -> list[str]:
    '''get a list of genres in the data sorted alphabetically.
    partial matches should be included '''
    genres = []
    for row in games:
        genre_split = row[2].split("/")
        for genre in genre_split:
            genre = genre.strip()
            if genre not in genres:
                genres.append(genre)
    n = len(genres)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if genres[j] < genres[min_index]:
                min_index = j
        genres[i], genres[min_index] = genres[min_index], genres[i]
    return genres

def games_by_sales(games, year) -> list[list[str]]:
    '''searches list of games for matches according to year inputted by user then ranked by sales'''
    game_by_year = []
    year = int(year)
    lines = []
    for line in games:
        if line[8] == year:
            lines.append(line)
    if not lines:
        return -1
    
    n = len(lines)
    for i in range(n-1):
        min_index = i
        for j in range(i+1, n):
            if lines[j][4] > lines[min_index][4]:
                min_index = j
        lines[i], lines[min_index] = lines[min_index], lines[i]
    return lines

def display(results: list[list[str]]) -> None:
    '''prints results in an 80 character wide window'''
    if results == -1:
        print("No results found")
        return
    else: 
        print(
            f"{'TITLE':15}|"
            f"{'REVIEW':10}|"
            f"{'SALES':10}|"
            f"{'PRICE':10}|"
            f"{'CONSOLE':10}|"
            f"{'YEAR':10}|"
            f"{'PLAYTIME':10}"
        )
        print("-" * 80)

        for row in results: 
            print(
                f"{row[0][0:15]:{15}}|"
                f"{row[3]:{10}}|"
                f"{row[4]:{10}}|"
                f"{row[5]:{10}}|"
                f"{row[6]:{10}}|"
                f"{row[8]:{10}}|"
                f"{row[9]:{10}}|"
            )
        number_matches = len(results)
        print(f'{number_matches} matches found')

main()
