# Setting Things up...
import requests
import time
from apikey import API_KEY
import sqlite3
from tabulate import tabulate

connection = sqlite3.connect(
    r"movies.db"
)  # --> give the correct database path
cursor = connection.cursor()


# Welcome Message
print("\n========== WELCOME TO THE MOVIE VAULT ==========\n")

# Program starts...
while True:
    try:
        user_perform = int(
            input(
                "What brings you here? Choose an option\n1. I wanna search a movie\n2. I wanna manage my watchlist\n3. Exit\n"
            )
        )
    except ValueError:
        print("\nPlease enter a valid number! (1,2,3)\n")
        continue
    if user_perform in [1,2,3]:

# Option 1 --> Searching a movie
        if user_perform == 1:
            movie_name = input("Enter movie you wanna search: ")

            try:
                request = requests.get("https://www.omdbapi.com/?",
                    params={"s": movie_name,"apikey": API_KEY},
                    timeout=10
                )
            except requests.exceptions.RequestException:
                print("Movie Vault is currently facing some problems. We'll be back soon 🔜\nPlease try again after few minutes\n")
                continue

            if request.status_code != 200:
                print("OOPS! An error occured. Please try again later...")
                continue
            else:
                try:
                    response = request.json()
                except requests.exceptions.JSONDecodeError:
                    print("⚠️ Received an unexpected response from the server. Please try again in a few minutes.")
                    continue
                response_code = response["Response"]
                if response_code == "False":
                    print(response["Error"])
                    continue
                else:
                    search = response.get("Search")
                    for i, j in enumerate(search, start=1):
                        print(f"{i}. {j["Title"]} ({j["Year"]})")
            while True:
                try:
                    user_choice = int(
                        input(
                            "\nChoose a movie number among these movies.\nType the movie number: \n"
                        )
                    )
                except ValueError:
                    print("Please choose a valid movie number")
                    continue
                if user_choice > len(search) or user_choice <=0:
                    print("\nPlease choose a valid movie number...")
                    continue
                break
            chosen_movie = search[user_choice - 1]
            movie_id = chosen_movie["imdbID"]
            try:
                request2 = requests.get(
                    f"https://www.omdbapi.com/?i={movie_id}&apikey={API_KEY}",timeout=11
                )
            except requests.exceptions.RequestException:
                print("Movie Vault is currently facing some problems. We'll be back soon 🔜\nPlease try again after few minutes\n")
                continue
            if request2.status_code != 200:
                print("OOPS! An error occured. Please try again later...")
                continue
            else:
                try:
                    movie_details = request2.json()
                except requests.exceptions.JSONDecodeError:
                    print("⚠️ Received an unexpected response from the server. Please try again in a few minutes.")
                    continue
                response_code2 = movie_details.get("Response")
                if response_code2 == "False":
                    print(movie_details["Error"])
                    continue
                else:
                    imdb_id = movie_details["imdbID"]
                    movie_name = movie_details["Title"].upper()
                    imdb_rating = movie_details["imdbRating"]
                    print(
                        f"\nTitle: {movie_name}\nYear: {movie_details["Year"]}\nGenre: {movie_details["Genre"]}\nPlot: {movie_details["Plot"]}\nDirector: {movie_details["Director"]}\nIMDb Rating: {imdb_rating}\nCast: {movie_details["Actors"]}\n"
                    )
                while True:
                    try:
                        save_or_not =int(input("Add this movie to watchlist? \n 1. YES\n 2. NO\n"))
                    except ValueError:
                        print("Please choose 1 or 2     (1 means YES , 2 means NO)\n")
                        continue
                    if save_or_not not in [1,2]:
                        print("Please choose a valid number\n")
                        continue
                    else:
                        break
            if save_or_not == 1:
                cursor.execute(
                    """SELECT * FROM MOVIES
                    WHERE IMDB_id IN (?);""",
                    (imdb_id,),
                )
                search_result = cursor.fetchone()
                if search_result == None:
                    cursor.execute(
                        """INSERT INTO MOVIES (IMDB_id,MOVIE_NAME,IMDB_RATING,WATCHED) VALUES(?,?,?,0);""",
                        (
                            imdb_id,
                            movie_name,
                            imdb_rating,
                        ),
                    )
                    connection.commit()
                    print("Movie added to watchlist successfully!\n")
                else:
                    print("Movie already exists in your watchlist...\n")
                continue

# Option 2 --> Managing the watchlist
        if user_perform == 2:
            while True:
                cursor.execute("""SELECT * FROM MOVIES;""")
                data = cursor.fetchall()
                watchlist = []
                for i in data:
                    i = list(i)
                    if i[-1] == 1:
                        i[-1] = "Watched"
                        watchlist.append(i)
                    else:
                        i[-1] = "Pending"
                        watchlist.append(i)
                print(
                    tabulate(
                        watchlist,
                        headers=["IMDB id", "Movie", "IMDB Rating", "Watched?"],
                        tablefmt="fancy_grid",
                        showindex=range(1, len(watchlist) + 1),
                    )
                )

                # manage watchlist
                while True:
                    try:
                        manage_choice = int(
                            input(
                                "📚 Manage Watchlist\nChoose an option\n1. Mark a movie as watched ✅\n2. Remove a movie\n3. Return to main menu 🔙\n"
                            )
                        )
                    except ValueError:
                        print("Please choose a valid number!!")
                        continue
                    if manage_choice not in [1,2,3]:
                        print("Please choose a valid number!!")
                        continue
                    else:
                        break
                if manage_choice == 1:
                    watched_name = input(
                        "Enter the movie name you wanna mark as watched:\n"
                    ).upper()
                
                    cursor.execute(
                        """SELECT * FROM MOVIES
                        WHERE MOVIE_NAME IN (?);""",
                        (watched_name,),
                    )
                    possible_movies1 = cursor.fetchall()

                    if len(possible_movies1) ==1:
                        cursor.execute(
                            """UPDATE MOVIES
                            SET WATCHED=1
                            WHERE MOVIE_NAME IN (?);""",
                            (watched_name,),
                        )
                        connection.commit()
                        print("Movie marked as watched ✅\n")

                    elif len(possible_movies1) > 1:
                        print(
                            tabulate(
                                possible_movies1,
                                headers=[
                                    "IMDBid",
                                    "Movie",
                                    "IMDB Rating",
                                    "Watched?",
                                ],
                                showindex=range(1, len(possible_movies1) + 1),
                                tablefmt="fancy_grid",
                            )
                        )
                        while True:
                            try:
                                exact_match_no1 = int(
                                    input(
                                        "Please select the movie number you wanna mark as watched: "
                                    )
                                )
                            except ValueError:
                                print("Please enter a valid number!")
                                continue
                            if exact_match_no1>len(possible_movies1) or exact_match_no1<=0:
                                print("Please enter a valid number!")
                                continue
                            else:
                                break
                        exact_match_movie1 = possible_movies1[exact_match_no1 - 1]
                        exact_match_movie_id1 = exact_match_movie1[0]
                        cursor.execute(
                             """UPDATE MOVIES
                                SET WATCHED=1
                                WHERE IMDB_id IN (?);""",
                                (exact_match_movie_id1,),
                            )
                        connection.commit()
                        print("Movie marked as watched ✅\n")

                    elif len(possible_movies1) == 0:
                        print(
                            "Movie not found! Please type the exact movie name\n"
                        )


                if manage_choice == 2:
                    remove_name = input(
                        "Enter the movie name you wanna remove:\n"
                    ).upper()
                    cursor.execute(
                        """SELECT * FROM MOVIES
                        WHERE MOVIE_NAME IN (?);""",
                        (remove_name,),
                    )
                    possible_movies2 = cursor.fetchall()

                    if len(possible_movies2) == 1:
                        cursor.execute(
                            """DELETE FROM MOVIES
                            WHERE MOVIE_NAME IN (?);""",
                            (remove_name,),
                        )
                        connection.commit()
                        print("\nMovie removed from watchlist.\n")

                    elif len(possible_movies2) > 1:
                        print(
                            tabulate(
                                possible_movies2,
                                headers=[
                                    "IMDBid",
                                    "Movie",
                                    "IMDB Rating",
                                    "Watched?",
                                ],
                                showindex=range(1, len(possible_movies2) + 1),
                                tablefmt="fancy_grid",
                            )
                        )
                        while True:
                            try:
                                exact_match_no2 = int(
                                    input(
                                        "Please select the movie number you wanna remove: "
                                    )
                                )
                            except ValueError:
                                print("Please enter a valid number!")
                                continue
                            if exact_match_no2>len(possible_movies2) or exact_match_no2<=0:
                                print("Please enter a valid number!")
                                continue
                            else:
                                break
                        exact_match_movie2 = possible_movies2[exact_match_no2 - 1]
                        exact_match_movie_id2 = exact_match_movie2[0]
                        cursor.execute(
                            """DELETE FROM MOVIES
                            WHERE IMDB_id IN (?);""",
                            (exact_match_movie_id2,),
                        )
                        connection.commit()
                        print("\nMovie removed from watchlist.\n")

                    elif len(possible_movies2) == 0:
                        print(
                            "Movie not found! Please type the exact movie name\n"
                        )

                if manage_choice == 3:
                    break

# Option 3 --> Leaving the application
        if user_perform == 3:
            leaving = input(
                "Leaving already? Are you sure you wanna exit?\nChoose yes or no (Y/N)\n"
            ).upper()
            if leaving == "YES" or leaving == "Y":
                print("Well, this is awkward...Anyways see you soon 👋")
                connection.close()
                exit()

    else:
        print("Please choose a valid option (1,2,3)\n")

# THE END OF CODE ... OR IS IT ? :)
