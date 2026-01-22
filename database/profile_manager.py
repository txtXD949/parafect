import json


class ProfileManager:
    def __init__(self):
        self.file_path: str = 'database/data.json'
        self.profiles: dict | None = self.load_profiles()

    def save_profiles(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=2)

    def load_profiles(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
        return {}

    def create_profile(self, user_id, name):
        self.profiles[str(user_id)] = self.create_default_profile(name)
        self.save_profiles()

    def save_profile(self, user_id, data):
        self.profiles[str(user_id)] = data
        self.save_profiles()

    def load_profile(self, user_id):
        return self.profiles.get(str(user_id))

    def update_name(self, user_id, name):
        profile = self.load_profile(user_id)
        if profile:
            profile['name'] = name
            self.save_profile(user_id, profile)
            return True
        return False

    def update_cash(self, user_id, amount, operation='add'):  # add / subtract / set
        profile = self.load_profile(user_id)

        if operation == 'add':
            profile['cash'] += amount
        if operation == 'subtract':
            profile['cash'] -= amount
        if operation == 'set':
            profile['cash'] = amount

        self.save_profile(user_id, profile)

    def update_level(self, user_id, level):
        profile = self.load_profile(user_id)

        profile['level'] = level
        self.save_profile(user_id, profile)

    def update_experience(self, user_id, exp):
        profile = self.load_profile(user_id)

        profile['experience'] = exp
        self.save_profile(user_id, profile)

    def update_inventory(self, user_id, item_name, value, operation='add'):  # add / subtract / set
        profile = self.load_profile(user_id)

        if item_name not in profile['inventory']:
            profile['inventory'][item_name] = 0

        if operation == 'add':
            profile['inventory'][item_name] += value
        elif operation == 'subtract':
            profile['inventory'][item_name] = max(0, profile['inventory'][item_name] - value)
        elif operation == 'set':
            profile['inventory'][item_name] = value

        self.save_profile(user_id, profile)

    def update_settings(self, user_id, setting_name, value):
        profile = self.load_profile(user_id)

        profile['settings'][setting_name] = value
        self.save_profile(user_id, profile)

    @staticmethod
    def create_default_profile(name='test_name'):
        """Создает JSON структуру профиля по умолчанию"""
        return {
            'name': name,
            'cash': 100,
            'level': 1,
            'experience': 0,
            'inventory': {
                'emf': 0,
                'uf': 0,
                'book': 0,
                'mic': 0,
                'dict': 0,
                'term': 0,
                'flash_light': 0,
                'camera': 0,
                'incense': 0,
                'lighter': 0,
                'pills': 0,
            },
            'settings': {
                'volume': 1.0,
                'ef_volume': 1.0,
                'language': 'ru'
            }
        }
