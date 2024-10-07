# localization.py

class Localization:
    def __init__(self):
        self.languages = {
            'en': {
                'welcome': "Welcome to Eco Poker Evolution!",
                'language_set': "Language set to English.",
                'start_game': "Game started by {}! Waiting for more players. Use !join to join the game.",
                'game_in_progress': "A game is already in progress!",
                'player_joined': "{} has joined the game! Total players: {}",
                'already_in_game': "You're already in the game!",
                'no_game_in_progress': "No game in progress. Use !start to start a new game."
                # Add more phrases as needed
            },
            'zh': {
                'welcome': "欢迎来到生态扑克进化游戏！",
                'language_set': "语言已设置为中文。",
                'start_game': "游戏由{}开始！等待更多玩家加入。使用!join加入游戏。",
                'game_in_progress': "游戏已经在进行中！",
                'player_joined': "{}已加入游戏！当前玩家数：{}",
                'already_in_game': "你已经在游戏中了！",
                'no_game_in_progress': "当前没有进行中的游戏。使用!start开始新游戏。"
                # 根据需要添加更多短语
            }
        }
        self.current_language = 'en'  # Default language

    def set_language(self, lang):
        if lang in self.languages:
            self.current_language = lang
            return self.get_text('language_set')
        return f"Unsupported language: {lang}"

    def get_text(self, key, *args):
        text = self.languages[self.current_language].get(key, key)
        return text.format(*args) if args else text

# 使用示例：
# localization = Localization()
# print(localization.get_text('welcome'))
# localization.set_language('zh')
# print(localization.get_text('welcome'))