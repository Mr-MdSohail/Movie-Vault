# Movie Vault 🎬

A command-line movie manager built with Python, SQLite, and the OMDb API.

Movie Vault allows users to search movies, view detailed movie information, save movies to a personal watchlist, and manage watched movies using a local SQLite database.

---

## Features

### 🔍 Search Movies

Search for movies using the OMDb API.

#### Workflow

1. Enter a movie title.
2. Movie Vault sends a request to the OMDb API.
3. Matching movies are displayed with numbered positions.
4. Select a movie from the list.
5. Proceed to view detailed movie information.

#### Example

```text
1. Inception (2010)
2. Interstellar (2014)
3. The Dark Knight (2008)

Choose a movie number:
```

#### Things to Remember

- A search can return multiple movies.
- Search results may be empty.
- Invalid movie selections are handled.
- Search results contain limited movie information.

---

### 🎬 View Movie Details

After selecting a movie, detailed information is retrieved using the movie's IMDb ID.

#### Information Displayed

- Title
- Year
- Genre
- Plot
- Director
- Cast
- IMDb Rating

#### Example

```text
Title: INTERSTELLAR

Year: 2014

Genre: Adventure, Drama, Sci‑Fi

Plot: A team of explorers travel through a wormhole in space...

Director: Christopher Nolan

Cast: Matthew McConaughey, Anne Hathaway

IMDb Rating: 8.7
```

#### Notes

- Movie details are fetched directly from the OMDb API.
- IMDb ID connects search results with the movie's complete record.
- No second title search is required.

---

### 💾 Add Movie to Watchlist

Save selected movies permanently in a local SQLite database.

#### Features

- Stores IMDb ID
- Stores movie title
- Stores IMDb rating
- Stores watched status
- Prevents duplicate movie entries

#### Workflow

1. Select a movie.
2. Choose whether to save it.
3. Check if the movie already exists.
4. If not present, save it to the database.
5. Confirm successful insertion.

#### Example

```text
Add this movie to watchlist?

1. YES
2. NO

Movie added to watchlist successfully!
```

---

### 📚 View and Manage Watchlist

View and manage saved movies.

#### Available Actions

- Mark movie as watched ✅
- Remove movie from watchlist 🗑️
- Return to main menu 🔙

#### Example Watchlist

```text
╒════════════╤═══════════════╤═════════════╤═══════════╕
│ IMDB ID    │ Movie         │ Rating      │ Watched?  │
╞════════════╪═══════════════╪═════════════╪═══════════╡
│ tt1375666  │ INCEPTION     │ 8.8         │ Pending   │
│ tt0816692  │ INTERSTELLAR  │ 8.7         │ Watched   │
╘════════════╧═══════════════╧═════════════╧═══════════╛
```

#### Workflow

1. Retrieve saved movies from SQLite.
2. Display watchlist.
3. Select an action.
4. Validate the movie and action.
5. Update or remove the movie.
6. Save changes.
7. Display confirmation.

---

## Technologies Used

- Python
- SQLite
- Requests
- Tabulate
- OMDb API

---

## Project Structure

```text
movie-vault/
│
├── main.py
├── create_table.sql
├── requirements.txt
├── apikey_example.py
└── README.md
```

---

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Create a file named:

```text
apikey.py
```

Add your OMDb API key:

```python
API_KEY = "YOUR_OMDB_API_KEY"
```

Run the application:

```bash
python main.py
```

---

## Database Structure

```sql
CREATE TABLE MOVIES (
    IMDB_ID TEXT PRIMARY KEY,
    MOVIE_NAME TEXT,
    IMDB_RATING REAL,
    WATCHED INTEGER DEFAULT 0
);
```

---

## Learning Goals

This project was built to practice:

- API Integration
- JSON Parsing
- SQLite Database Operations
- CRUD Operations
- Error Handling
- User Input Validation
- Python Project Structure

---

## Author

Built by Md Sohail while learning Python, SQLite, APIs, and CLI application development.
