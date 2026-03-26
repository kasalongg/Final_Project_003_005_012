from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from typing import List, Optional

# Database Configuration
DB_CONFIG = {
    'host': '192.168.100.5',
    'port': 3306,
    'database': 'sport',
    'user': 'root',
    'password': 'P@ssw0rd'
}

app = FastAPI()

# Database Connection Helper
def get_db_connection():
    """Create and return a MySQL connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Sport API", "version": "1.0"}

# Pydantic Models
class Team(BaseModel):
    id: Optional[int] = None
    team_name: str

class TeamResponse(BaseModel):
    id: int
    team_name: str

class Athlete(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    team_id: int

class AthleteResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    team_id: int

class Sport(BaseModel):
    id: Optional[int] = None
    sport_name: str

class SportResponse(BaseModel):
    id: int
    sport_name: str

class Match(BaseModel):
    id: Optional[int] = None
    sport_id: int
    team_a_id: int
    team_b_id: int
    match_date: str
    match_time: str

class MatchResponse(BaseModel):
    id: int
    sport_id: int
    team_a_id: int
    team_b_id: int
    match_date: str
    match_time: str

class Medal(BaseModel):
    id: Optional[int] = None
    team_id: int
    sport_id: int
    gold_count: int
    silver_count: int
    bronze_count: int

class MedalResponse(BaseModel):
    id: int
    team_id: int
    sport_id: int
    gold_count: int
    silver_count: int
    bronze_count: int

class Leaderboard(BaseModel):
    id: Optional[int] = None
    team_id: int
    total_gold: int
    total_silver: int
    total_bronze: int
    total_score: int

class LeaderboardResponse(BaseModel):
    id: int
    team_id: int
    total_gold: int
    total_silver: int
    total_bronze: int
    total_score: int

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# ======================
# USERS CRUD
# ======================

@app.get("/users", response_model=List[UserResponse])
async def get_all_users():
    """Retrieve all users from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id as id, username, password FROM user")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return users
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int):
    """Retrieve a specific user by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id as id, username, password FROM user WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        return user
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/users", response_model=UserResponse)
async def create_user(user: User):
    """Create a new user in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO user (username, password) VALUES (%s, %s)",
            (user.username, user.password)
        )
        connection.commit()
        user_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": user_id_last, "username": user.username, "password": user.password}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: User):
    """Update an existing user"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT user_id FROM user WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        
        # Update the user
        cursor.execute(
            "UPDATE user SET username = %s, password = %s WHERE user_id = %s",
            (user.username, user.password, user_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": user_id, "username": user.username, "password": user.password}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT user_id FROM user WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        
        # Delete the user
        cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"User with id {user_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/user_login")
async def user_login(login_request: LoginRequest):
    """Login user - check credentials and auto-register if needed"""
    try:
        username = login_request.username.strip() if login_request.username else ""
        password = login_request.password.strip() if login_request.password else ""
        
        if not username or not password:
            return {"success": False, "message": "Username and password required", "user_id": None}
        
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if user exists
        cursor.execute("SELECT user_id as id, username, password FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            # User exists - check password
            stored_password = str(user.get('password', '')).strip()
            input_password = str(password).strip()
            
            if stored_password == input_password:
                # Login successful
                cursor.close()
                connection.close()
                return {
                    "success": True,
                    "message": "Login successful",
                    "user_id": int(user.get('id')),
                    "username": user.get('username')
                }
            else:
                # Wrong password
                cursor.close()
                connection.close()
                return {"success": False, "message": "Invalid username or password", "user_id": None}
        else:
            # User doesn't exist - auto-register (create new user)
            try:
                cursor.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)",
                    (username, password)
                )
                connection.commit()
                new_user_id = cursor.lastrowid
                cursor.close()
                connection.close()
                
                return {
                    "success": True,
                    "message": "Account created successfully",
                    "user_id": new_user_id,
                    "username": username
                }
            except Error as insert_error:
                cursor.close()
                connection.close()
                raise HTTPException(status_code=500, detail=f"Registration failed: {str(insert_error)}")
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}", "user_id": None}

# ======================
# TEAMS CRUD
# ======================

@app.get("/teams", response_model=List[TeamResponse])
async def get_all_teams():
    """Retrieve all teams from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT team_id as id, team_name FROM teams")
        teams = cursor.fetchall()
        cursor.close()
        connection.close()
        return teams
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team_by_id(team_id: int):
    """Retrieve a specific team by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT team_id as id, team_name FROM teams WHERE team_id = %s", (team_id,))
        team = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not team:
            raise HTTPException(status_code=404, detail=f"Team with id {team_id} not found")
        return team
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/teams", response_model=TeamResponse)
async def create_team(team: Team):
    """Create a new team in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO teams (team_name) VALUES (%s)",
            (team.team_name,)
        )
        connection.commit()
        team_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": team_id_last, "team_name": team.team_name}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/teams/{team_id}", response_model=TeamResponse)
async def update_team(team_id: int, team: Team):
    """Update an existing team"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if team exists
        cursor.execute("SELECT team_id FROM teams WHERE team_id = %s", (team_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Team with id {team_id} not found")
        
        # Update the team
        cursor.execute(
            "UPDATE teams SET team_name = %s WHERE team_id = %s",
            (team.team_name, team_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": team_id, "team_name": team.team_name}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/teams/{team_id}")
async def delete_team(team_id: int):
    """Delete a team from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if team exists
        cursor.execute("SELECT team_id FROM teams WHERE team_id = %s", (team_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Team with id {team_id} not found")
        
        # Delete the team
        cursor.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"Team with id {team_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ======================
# ATHLETES CRUD
# ======================

@app.get("/athletes", response_model=List[AthleteResponse])
async def get_all_athletes():
    """Retrieve all athletes from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT athletes_id as id, first_name, last_name, team_id FROM athletes")
        athletes = cursor.fetchall()
        cursor.close()
        connection.close()
        return athletes
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/athletes/{athlete_id}", response_model=AthleteResponse)
async def get_athlete_by_id(athlete_id: int):
    """Retrieve a specific athlete by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT athletes_id as id, first_name, last_name, team_id FROM athletes WHERE athletes_id = %s", (athlete_id,))
        athlete = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not athlete:
            raise HTTPException(status_code=404, detail=f"Athlete with id {athlete_id} not found")
        return athlete
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/athletes", response_model=AthleteResponse)
async def create_athlete(athlete: Athlete):
    """Create a new athlete in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO athletes (first_name, last_name, team_id) VALUES (%s, %s, %s)",
            (athlete.first_name, athlete.last_name, athlete.team_id)
        )
        connection.commit()
        athlete_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": athlete_id_last, "first_name": athlete.first_name, "last_name": athlete.last_name, "team_id": athlete.team_id}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/athletes/{athlete_id}", response_model=AthleteResponse)
async def update_athlete(athlete_id: int, athlete: Athlete):
    """Update an existing athlete"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if athlete exists
        cursor.execute("SELECT athletes_id FROM athletes WHERE athletes_id = %s", (athlete_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Athlete with id {athlete_id} not found")
        
        # Update the athlete
        cursor.execute(
            "UPDATE athletes SET first_name = %s, last_name = %s, team_id = %s WHERE athletes_id = %s",
            (athlete.first_name, athlete.last_name, athlete.team_id, athlete_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": athlete_id, "first_name": athlete.first_name, "last_name": athlete.last_name, "team_id": athlete.team_id}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/athletes/{athlete_id}")
async def delete_athlete(athlete_id: int):
    """Delete an athlete from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if athlete exists
        cursor.execute("SELECT athletes_id FROM athletes WHERE athletes_id = %s", (athlete_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Athlete with id {athlete_id} not found")
        
        # Delete the athlete
        cursor.execute("DELETE FROM athletes WHERE athletes_id = %s", (athlete_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"Athlete with id {athlete_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ======================
# SPORTS CRUD
# ======================

@app.get("/sports", response_model=List[SportResponse])
async def get_all_sports():
    """Retrieve all sports from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT sport_id as id, sport_name FROM sports")
        sports = cursor.fetchall()
        cursor.close()
        connection.close()
        return sports
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/sports/{sport_id}", response_model=SportResponse)
async def get_sport_by_id(sport_id: int):
    """Retrieve a specific sport by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT sport_id as id, sport_name FROM sports WHERE sport_id = %s", (sport_id,))
        sport = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not sport:
            raise HTTPException(status_code=404, detail=f"Sport with id {sport_id} not found")
        return sport
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/sports", response_model=SportResponse)
async def create_sport(sport: Sport):
    """Create a new sport in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO sports (sport_name) VALUES (%s)",
            (sport.sport_name,)
        )
        connection.commit()
        sport_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": sport_id_last, "sport_name": sport.sport_name}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/sports/{sport_id}", response_model=SportResponse)
async def update_sport(sport_id: int, sport: Sport):
    """Update an existing sport"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if sport exists
        cursor.execute("SELECT sport_id FROM sports WHERE sport_id = %s", (sport_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Sport with id {sport_id} not found")
        
        # Update the sport
        cursor.execute(
            "UPDATE sports SET sport_name = %s WHERE sport_id = %s",
            (sport.sport_name, sport_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": sport_id, "sport_name": sport.sport_name}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/sports/{sport_id}")
async def delete_sport(sport_id: int):
    """Delete a sport from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if sport exists
        cursor.execute("SELECT sport_id FROM sports WHERE sport_id = %s", (sport_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Sport with id {sport_id} not found")
        
        # Delete the sport
        cursor.execute("DELETE FROM sports WHERE sport_id = %s", (sport_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"Sport with id {sport_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ======================
# MATCHES CRUD
# ======================

@app.get("/matches", response_model=List[MatchResponse])
async def get_all_matches():
    """Retrieve all matches from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT match_id as id, sport_id, team_a_id, team_b_id, match_date, match_time FROM matches")
        matches = cursor.fetchall()
        cursor.close()
        connection.close()
        return matches
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/matches/{match_id}", response_model=MatchResponse)
async def get_match_by_id(match_id: int):
    """Retrieve a specific match by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT match_id as id, sport_id, team_a_id, team_b_id, match_date, match_time FROM matches WHERE match_id = %s", (match_id,))
        match = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not match:
            raise HTTPException(status_code=404, detail=f"Match with id {match_id} not found")
        return match
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/matches", response_model=MatchResponse)
async def create_match(match: Match):
    """Create a new match in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO matches (sport_id, team_a_id, team_b_id, match_date, match_time) VALUES (%s, %s, %s, %s, %s)",
            (match.sport_id, match.team_a_id, match.team_b_id, match.match_date, match.match_time)
        )
        connection.commit()
        match_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": match_id_last, "sport_id": match.sport_id, "team_a_id": match.team_a_id, "team_b_id": match.team_b_id, "match_date": match.match_date, "match_time": match.match_time}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/matches/{match_id}", response_model=MatchResponse)
async def update_match(match_id: int, match: Match):
    """Update an existing match"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if match exists
        cursor.execute("SELECT match_id FROM matches WHERE match_id = %s", (match_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Match with id {match_id} not found")
        
        # Update the match
        cursor.execute(
            "UPDATE matches SET sport_id = %s, team_a_id = %s, team_b_id = %s, match_date = %s, match_time = %s WHERE match_id = %s",
            (match.sport_id, match.team_a_id, match.team_b_id, match.match_date, match.match_time, match_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": match_id, "sport_id": match.sport_id, "team_a_id": match.team_a_id, "team_b_id": match.team_b_id, "match_date": match.match_date, "match_time": match.match_time}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/matches/{match_id}")
async def delete_match(match_id: int):
    """Delete a match from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if match exists
        cursor.execute("SELECT match_id FROM matches WHERE match_id = %s", (match_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Match with id {match_id} not found")
        
        # Delete the match
        cursor.execute("DELETE FROM matches WHERE match_id = %s", (match_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"Match with id {match_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ======================
# MEDALS CRUD
# ======================

@app.get("/medals", response_model=List[MedalResponse])
async def get_all_medals():
    """Retrieve all medals from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT medal_id as id, team_id, sport_id, gold_count, silver_count, bronze_count FROM medals")
        medals = cursor.fetchall()
        cursor.close()
        connection.close()
        return medals
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/medals/{medal_id}", response_model=MedalResponse)
async def get_medal_by_id(medal_id: int):
    """Retrieve a specific medal by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT medal_id as id, team_id, sport_id, gold_count, silver_count, bronze_count FROM medals WHERE medal_id = %s", (medal_id,))
        medal = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not medal:
            raise HTTPException(status_code=404, detail=f"Medal with id {medal_id} not found")
        return medal
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/medals", response_model=MedalResponse)
async def create_medal(medal: Medal):
    """Create a new medal record in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO medals (team_id, sport_id, gold_count, silver_count, bronze_count) VALUES (%s, %s, %s, %s, %s)",
            (medal.team_id, medal.sport_id, medal.gold_count, medal.silver_count, medal.bronze_count)
        )
        connection.commit()
        medal_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": medal_id_last, "team_id": medal.team_id, "sport_id": medal.sport_id, "gold_count": medal.gold_count, "silver_count": medal.silver_count, "bronze_count": medal.bronze_count}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/medals/{medal_id}", response_model=MedalResponse)
async def update_medal(medal_id: int, medal: Medal):
    """Update an existing medal record"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if medal exists
        cursor.execute("SELECT medal_id FROM medals WHERE medal_id = %s", (medal_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Medal with id {medal_id} not found")
        
        # Update the medal
        cursor.execute(
            "UPDATE medals SET team_id = %s, sport_id = %s, gold_count = %s, silver_count = %s, bronze_count = %s WHERE medal_id = %s",
            (medal.team_id, medal.sport_id, medal.gold_count, medal.silver_count, medal.bronze_count, medal_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": medal_id, "team_id": medal.team_id, "sport_id": medal.sport_id, "gold_count": medal.gold_count, "silver_count": medal.silver_count, "bronze_count": medal.bronze_count}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/medals/{medal_id}")
async def delete_medal(medal_id: int):
    """Delete a medal record from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if medal exists
        cursor.execute("SELECT medal_id FROM medals WHERE medal_id = %s", (medal_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Medal with id {medal_id} not found")
        
        # Delete the medal
        cursor.execute("DELETE FROM medals WHERE medal_id = %s", (medal_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"Medal with id {medal_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ======================
# LEADERBOARD CRUD
# ======================

@app.get("/leaderboard", response_model=List[LeaderboardResponse])
async def get_all_leaderboard():
    """Retrieve all leaderboard records from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT leaderboard_id as id, team_id, total_gold, total_silver, total_bronze, total_score FROM leaderboard")
        leaderboards = cursor.fetchall()
        cursor.close()
        connection.close()
        return leaderboards
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/leaderboard/{leaderboard_id}", response_model=LeaderboardResponse)
async def get_leaderboard_by_id(leaderboard_id: int):
    """Retrieve a specific leaderboard record by ID"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT leaderboard_id as id, team_id, total_gold, total_silver, total_bronze, total_score FROM leaderboard WHERE leaderboard_id = %s", (leaderboard_id,))
        leaderboard = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not leaderboard:
            raise HTTPException(status_code=404, detail=f"Leaderboard with id {leaderboard_id} not found")
        return leaderboard
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/leaderboard", response_model=LeaderboardResponse)
async def create_leaderboard(leaderboard: Leaderboard):
    """Create a new leaderboard record in the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO leaderboard (team_id, total_gold, total_silver, total_bronze, total_score) VALUES (%s, %s, %s, %s, %s)",
            (leaderboard.team_id, leaderboard.total_gold, leaderboard.total_silver, leaderboard.total_bronze, leaderboard.total_score)
        )
        connection.commit()
        leaderboard_id_last = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return {"id": leaderboard_id_last, "team_id": leaderboard.team_id, "total_gold": leaderboard.total_gold, "total_silver": leaderboard.total_silver, "total_bronze": leaderboard.total_bronze, "total_score": leaderboard.total_score}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/leaderboard/{leaderboard_id}", response_model=LeaderboardResponse)
async def update_leaderboard(leaderboard_id: int, leaderboard: Leaderboard):
    """Update an existing leaderboard record"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if leaderboard exists
        cursor.execute("SELECT leaderboard_id FROM leaderboard WHERE leaderboard_id = %s", (leaderboard_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Leaderboard with id {leaderboard_id} not found")
        
        # Update the leaderboard
        cursor.execute(
            "UPDATE leaderboard SET team_id = %s, total_gold = %s, total_silver = %s, total_bronze = %s, total_score = %s WHERE leaderboard_id = %s",
            (leaderboard.team_id, leaderboard.total_gold, leaderboard.total_silver, leaderboard.total_bronze, leaderboard.total_score, leaderboard_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"id": leaderboard_id, "team_id": leaderboard.team_id, "total_gold": leaderboard.total_gold, "total_silver": leaderboard.total_silver, "total_bronze": leaderboard.total_bronze, "total_score": leaderboard.total_score}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/leaderboard/{leaderboard_id}")
async def delete_leaderboard(leaderboard_id: int):
    """Delete a leaderboard record from the database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Check if leaderboard exists
        cursor.execute("SELECT leaderboard_id FROM leaderboard WHERE leaderboard_id = %s", (leaderboard_id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Leaderboard with id {leaderboard_id} not found")
        
        # Delete the leaderboard
        cursor.execute("DELETE FROM leaderboard WHERE leaderboard_id = %s", (leaderboard_id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": f"Leaderboard with id {leaderboard_id} deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Server run configuration
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3500)