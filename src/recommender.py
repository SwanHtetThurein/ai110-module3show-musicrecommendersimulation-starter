from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Convert songs to dictionaries and score them
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
        }
        
        scored_songs = []
        for song in self.songs:
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored_songs.append((song, score))
        
        # Sort by score descending and return top k
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # Convert user and song to the format needed for scoring
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
        }
        
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness,
        }
        
        score, reasons = score_song(user_prefs, song_dict)
        explanation = f"{song.title} by {song.artist} (Score: {score:.1f})\n"
        explanation += "\n".join(f"  • {reason}" for reason in reasons)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    df = pd.read_csv(csv_path)
    # Convert each row to a dictionary and convert numeric types as needed
    songs = []
    for _, row in df.iterrows():
        song = {
            'id': int(row['id']),
            'title': row['title'],
            'artist': row['artist'],
            'genre': row['genre'],
            'mood': row['mood'],
            'energy': float(row['energy']),
            'tempo_bpm': float(row['tempo_bpm']),
            'valence': float(row['valence']),
            'danceability': float(row['danceability']),
            'acousticness': float(row['acousticness']),
        }
        songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    Expected return format: (score, reasons)
    """
    score = 0.0
    reasons = []
    
    # Genre match (30 points)
    if song['genre'].lower() == user_prefs.get('genre', '').lower():
        score += 30
        reasons.append(f"Matches your genre preference ({user_prefs['genre']})")
    
    # Mood match (30 points)
    if song['mood'].lower() == user_prefs.get('mood', '').lower():
        score += 30
        reasons.append(f"Matches your mood preference ({user_prefs['mood']})")
    
    # Energy similarity (20 points) - closer to target energy is better
    target_energy = user_prefs.get('energy', 0.5)
    energy_diff = abs(song['energy'] - target_energy)
    energy_score = max(0, 20 - (energy_diff * 20))  # Linear decay based on difference
    score += energy_score
    reasons.append(f"Energy level {song['energy']:.2f} (your target: {target_energy:.2f})")
    
    # Acousticness preference (20 points)
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    if likes_acoustic and song['acousticness'] > 0.6:
        score += 15
        reasons.append(f"Acoustic quality matches your preference")
    elif not likes_acoustic and song['acousticness'] < 0.4:
        score += 15
        reasons.append(f"Non-acoustic style matches your preference")
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    Expected return format: (song_dict, score, explanation)
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " • ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k
    return scored_songs[:k]
