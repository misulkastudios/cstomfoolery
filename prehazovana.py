import os
import json
import random

class Character:
    def __init__(self, name, team, stamina, height, optimism, catching, special_ability=None):
        self.name = name
        self.team = team
        self.stamina = stamina
        self.height = height
        self.optimism = optimism
        self.catching = catching
        self.special_ability = special_ability

    def dunk_chance(self):
        return min(0.9 + self.height * 0.05, 1.0)

    def apply_special_ability(self, other_player):
        if self.special_ability == "Optimist":
            self.optimism = 100
            other_player.team.optimism *= 1.5
        elif self.special_ability == "Joker":
            return random.random() <= 0.35
        elif self.special_ability == "Rage":
            if self.team.optimism < other_player.team.optimism:
                self.stamina *= 1.2
                self.height *= 1.1

class Team:
    def __init__(self, name, optimism):
        self.name = name
        self.optimism = optimism

class Game:
    def __init__(self):
        self.characters = []
        self.teams = {}

    def load_characters(self):
        characters_folder = 'characters'
        team_folders = ['Red', 'Blue']  # Update team folders accordingly

        if not os.path.exists(characters_folder):
            os.makedirs(characters_folder)
            for folder in team_folders:
                os.makedirs(os.path.join(characters_folder, folder))

        for folder in team_folders:
            team_path = os.path.join(characters_folder, folder)
            files = os.listdir(team_path)
            valid_characters = []

            for file in files:
                file_path = os.path.join(team_path, file)
                if file.endswith('.json'):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        character = Character(data['name'], data['team'], data['stamina'], data['height'], data['optimism'], data['catching'], data.get('special_ability'))
                        if len(valid_characters) < 2:  # Load only 2 characters per team
                            valid_characters.append(character)
                        if data['team'] not in self.teams:
                            self.teams[data['team']] = Team(data['team'], data['optimism'])

            if len(valid_characters) == 2:  # Ensure exactly 2 characters per team
                self.characters.extend(valid_characters)
                print(f"{folder} loaded successfully with 2 valid characters.")
            else:
                print(f"Error: {folder} folder does not contain exactly 2 valid character files.")
                return

    def show_characters(self):
        print("Available Characters:")
        for idx, character in enumerate(self.characters, start=1):
            print(f"{idx}. {character.name} - Team: {character.team}")

    def throw_ball(self, character):
        selection = input(f"\nSelect ball throw type for {character.name}: [Low/Mid/High] ").lower()
        if selection not in ['low', 'mid', 'high']:
            print("Invalid selection.")
            return

        hit_chance = {
            'low': 0.3,
            'mid': 0.6,
            'high': 0.9
        }

        catch_chance = character.catching * 0.1

        throw_type = selection
        hit_prob = hit_chance[throw_type]

        if random.random() <= hit_prob:
            print(f"{character.name} throws the ball {throw_type} and scores a point for Team {character.team}!")
            return True
        else:
            print(f"{character.name} throws the ball {throw_type}, but it misses!")

            if random.random() <= catch_chance:
                print("The enemy team catches the ball!")
            return False

    def play_game(self):
        print("Welcome to Přehazovaná!")
        self.load_characters()
        self.show_characters()

        score_team1 = 0
        score_team2 = 0

        # Simulate movement clockwise in the game loop
        current_position = 0
        positions = ['Middle Back', 'Left Back', 'Left Front', 'Middle Front', 'Right Front', 'Right Back']

        while True:
            print(f"\nPosition: {positions[current_position]}")
            current_position = (current_position + 1) % len(positions)

            # Select characters from different teams randomly
            team_1_characters = [character for character in self.characters if character.team == 'Red']
            team_2_characters = [character for character in self.characters if character.team == 'Blue']

            if not team_1_characters or not team_2_characters:
                print("Error: Both teams must have available characters.")
                break

            character1 = random.choice(team_1_characters)
            character2 = random.choice(team_2_characters)

            print(f"\n{character1.name} from Team {character1.team} vs {character2.name} from Team {character2.team}")

            # Perform action between the characters
            if random.choice([True, False]):
                attacking_character = character1
                defending_character = character2
            else:
                attacking_character = character2
                defending_character = character1

            # Calculate chance of successful hit based on character's stats
            if self.throw_ball(attacking_character):
                if attacking_character.team == 'Red':
                    score_team1 += 1
                else:
                    score_team2 += 1

            print(f"The score is {score_team1}:{score_team2} for Team Red:Team Blue\n")

def main():
    game = Game()
    game.play_game()

if __name__ == "__main__":
    main()
