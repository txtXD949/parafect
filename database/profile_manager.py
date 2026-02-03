import json


class ProfileManager:
    """Менеджер для работы с профилями"""

    def __init__(self) -> None:
        self.file_path: str = 'database/data.json'
        self.profiles: dict | None = self.load_profiles()

    def save_profiles(self) -> None:
        """Сохраняет профили в data.json"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=2)

    def load_profiles(self) -> dict | None:
        """Выгружает профили из data.json"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
        return {}

    def create_profile(self, user_id, name) -> None:
        """Создает профиль"""
        self.profiles[str(user_id)] = self.create_default_profile(name)
        self.save_profiles()

    def save_profile(self, user_id, data) -> None:
        """Сохраняет профиль и передает в self.save_profiles"""
        self.profiles[str(user_id)] = data
        self.save_profiles()

    def load_profile(self, user_id) -> dict | None:
        """Выгружает один профиль"""
        return self.profiles.get(str(user_id))

    def update_name(self, user_id, name) -> bool:
        """Обновляет имя профиля"""
        profile = self.load_profile(user_id)
        if profile:
            profile['name'] = name
            self.save_profile(user_id, profile)
            return True
        return False

    def update_cash(self, user_id, amount, operation='add') -> None:  # add / subtract / set
        """Обновляет баланс"""
        profile = self.load_profile(user_id)

        if operation == 'add':
            profile['cash'] += amount
        if operation == 'subtract':
            profile['cash'] -= amount
        if operation == 'set':
            profile['cash'] = amount

        self.save_profile(user_id, profile)

    def update_level(self, user_id, level) -> None:
        """Обновляет уровень"""
        profile = self.load_profile(user_id)

        profile['level'] = level
        self.save_profile(user_id, profile)

    def update_experience(self, user_id, exp) -> None:
        """Обновляет опыт"""
        profile = self.load_profile(user_id)

        profile['experience'] = exp
        self.save_profile(user_id, profile)

    def update_inventory(self, user_id, item_name, value, operation='add') -> None:  # add / subtract / set
        """Обновляет инвентарь"""
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

    @staticmethod
    def create_default_profile(name: str) -> dict:
        """Создает JSON структуру профиля по умолчанию"""
        return {
            'name': name,
            'cash': 100,
            'level': 1,
            'experience': 0,
            'inventory': {
                'emf': 0,
                'low_light': 0,
                'book': 0,
                'mic': 0,
                'dict': 0,
                'term': 0,
                'flash_light': 0,
                'incense': 0,
                'lighter': 0,
                'pills': 0,
            }
        }
