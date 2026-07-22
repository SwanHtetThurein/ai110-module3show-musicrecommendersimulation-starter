# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This recommender system uses a weighted scoring algorithm that evaluates songs across multiple dimensions to match user preferences:

**Song Features Used:**
- Genre (categorical) - matched exactly to user preference
- Mood (categorical) - matched exactly to user preference  
- Energy (0-1 scale) - scored based on similarity to user's target energy level
- Acousticness (0-1 scale) - bonus points if it matches user's acoustic preference

**User Profile:**
The system stores four user preference attributes:
- `favorite_genre` - preferred music genre (e.g., "pop", "lofi", "rock")
- `favorite_mood` - preferred mood (e.g., "happy", "chill", "intense")
- `target_energy` - desired energy level (0-1 scale)
- `likes_acoustic` - boolean preference for acoustic vs. non-acoustic music

**Scoring Algorithm:**
The recommender calculates a score for each song:
- **+30 points** if genre exactly matches user preference
- **+30 points** if mood exactly matches user preference
- **Up to +20 points** based on energy similarity (linear decay based on difference from target)
- **Up to +15 points** for acousticness alignment (high points if acoustic preference matches)

**Recommendation Selection:**
1. Scores all songs against the user profile
2. Sorts songs by score in descending order
3. Returns the top k songs with explanations of why each was recommended

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
User profile: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

Top recommendations:

Sunrise City - Score: 94.60
Because: Matches your genre preference (pop) • Matches your mood preference (happy) 
• Energy level 0.82 (your target: 0.80) • Non-acoustic style matches your preference

Rooftop Lights - Score: 64.20
Because: Matches your mood preference (happy) • Energy level 0.76 (your target: 0.80) 
• Non-acoustic style matches your preference

Gym Hero - Score: 62.40
Because: Matches your genre preference (pop) • Energy level 0.93 (your target: 0.80) 
• Non-acoustic style matches your preference

Ni**Genre + Mood weight**: The current system gives equal weight (30 points each) to genre and mood matching. This ensures exact preference matches are heavily rewarded.
- **Energy similarity scoring**: Linear decay was chosen so songs within ±0.1 of the target energy receive significant credit, while increasingly different energies receive less.
- **Acousticness preference**: Implemented as a threshold-based bonus (high acousticness >0.6 vs. low acousticness <0.4) rather than a continuous scale to give clearer preferences.
- **K=5 recommendations**: Limited to top 5 results to balance providing variety while keeping the list manageable.
Storm Runner - Score: 32.80
Because: Energy level 0.91 (your target: 0.80) • Non-acoustic style matches your preference
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.
**Current Limitations:**
- **Limited features**: Uses only 4 features for scoring. Ignores tempo, valence, and danceability which could provide more nuanced recommendations.
- **No collaborative filtering**: Recommends based only on individual user preferences, not on patterns from similar users.
- **Cold start problem**: New users with no preference history cannot be effectively recommended to.
- **Binary acousticness**: Uses simple thresholds (>0.6, <0.4) rather than treating acousticness as a continuous preference dimension.
- **No temporal trends**: Doesn't account for what the user might want to listen to at different times of day.
- **Small dataset**: Only 10 songs in the training set, so diversity in recommendations is limited.

**How This Mirrors Real-World Systems:**
Real recommenders like Spotify face similar challenges: they balance explicit user preferences with implicit signals (listen history, skip patterns), deal with new user onboarding, and must manage computational efficiency at scale. Our simple system demonstrates the core trade-off: simpler scoring is interpretable and fast, but misses nuanced patterns that more complex models could capture.
Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



