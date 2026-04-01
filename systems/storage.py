import os, json
from data.profile import Profile

class Storage:
    def __init__(self, filepath="data.json"):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            data = {
                "profiles": [],
                "leaderboard": []
            }
            self._write(data)
    
    def _read(self):
        with open(self.filepath, "r") as file:
            return json.load(file)
        
    def _write(self, data):
        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)

    def get_profiles(self):
        data = self._read()
        return [Profile.from_dict(p) for p in data["profiles"]]
    
    def get_profile(self, name):
        profiles = self.get_profiles()
        for p in profiles:
            if p.name == name:
                return p
        
        return None

    def save_profile(self, profile: Profile):
        data = self._read()
        profiles = data["profiles"]

        updated = False

        for i, p in enumerate(profiles):
            if p["name"] == profile.name:
                profiles[i] = profile.to_dict()
                updated = True
                break
                
        if not updated:
            profiles.append(profile.to_dict())

        data["profiles"] = profiles
        self._write(data)
    
    def create_profile(self, name):
        profile = Profile(name)
        self.save_profile(profile)
        return profile
    
    def get_leaderboard(self):
        data = self._read()
        return data["leaderboard"]
    
    def update_leaderboard(self, name, score):
        if score <= 0:
            return False
    
        data = self._read()
        leaderboard = data["leaderboard"]

        leaderboard.append({
            "name": name,
            "score": score
        })

        # descending  sort, lambda is used to access and sort by "score" to avoid using helper function
        leaderboard.sort(key=lambda x: x["score"], reverse=True) 

        # keeping top 3
        leaderboard = leaderboard[:3] 

        data["leaderboard"] = leaderboard
        self._write(data)

        return any(entry["name"] == name and entry["score"] == score for entry in leaderboard)
        
    def update_profile_stats(self, profile, score, level, food_type=None):
        if score > profile.high_score:
            profile.high_score = score
        
        if level > profile.max_level:
            profile.max_level = level
        
        if food_type:
            profile.food_stats[food_type] += 1

        self.save_profile(profile)
