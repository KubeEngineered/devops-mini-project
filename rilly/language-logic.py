class RillyApp:
    def __init__(self):
        # Default language setting
        self.current_lang = "en"
        
        # Supported languages
        self.languages = {
            "en": "English",
            "hi": "हिंदी (Hindi)",
            "mr": "मराठी (Marathi)"
        }
        
        # UI Translations Dictionary
        self.translations = {
            "en": {
                "welcome": "Welcome back to Rilly!",
                "daily_goal": "Your daily goal: 8,000 steps.",
                "water_intake": "Water intake: 2.5 L logged.",
                "settings_menu": "\n--- Settings ---",
                "select_lang": "Choose language:\n1. English\n2. Hindi (हिंदी)\n3. Marathi (मराठी)\nEnter choice (1-3): ",
                "lang_changed": "Language successfully changed to English!",
                "invalid_choice": "Invalid choice. Keeping current language.",
                "menu_prompt": "\n1. View Dashboard\n2. Change Language\n3. Exit\nChoose an option: "
            },
            "hi": {
                "welcome": "रिल्ली (Rilly) में आपका फिर से स्वागत है!",
                "daily_goal": "आपका दैनिक लक्ष्य: 8,000 कदम।",
                "water_intake": "पानी का सेवन: 2.5 लीटर लॉग किया गया।",
                "settings_menu": "\n--- सेटिंग्स ---",
                "select_lang": "भाषा चुनें:\n1. English\n2. हिंदी\n3. मराठी\nविकल्प चुनें (1-3): ",
                "lang_changed": "भाषा सफलतापूर्वक हिंदी में बदल दी गई है!",
                "invalid_choice": "अमान्य विकल्प। वर्तमान भाषा रखी जा रही है।",
                "menu_prompt": "\n1. डैशबोर्ड देखें\n2. भाषा बदलें\n3. बाहर निकलें\nविकल्प चुनें: "
            },
            "mr": {
                "welcome": "रिल्ली (Rilly) मध्ये आपले पुन्हा स्वागत आहे!",
                "daily_goal": "आपले दैनंदिन ध्येय: ८,००० पावले.",
                "water_intake": "पाणी पिण्याची नोंद: २.५ लीटर.",
                "settings_menu": "\n--- सेटिंग्ज ---",
                "select_lang": "भाषा निवडा:\n1. English\n2. हिंदी\n3. मराठी\nपर्याय निवडा (1-3): ",
                "lang_changed": "भाषा यशस्वीरित्या मराठीमध्ये बदलली आहे!",
                "invalid_choice": "अवैध पर्याय. सध्याची भाषा ठेवली जात आहे.",
                "menu_prompt": "\n1. डॅशबोर्ड पहा\n2. भाषा बदला\n3. बाहेर पडा\nपर्याय निवडा: "
            }
        }

    def t(self, key: str) -> str:
        """Helper method to get translated string for current language."""
        return self.translations.get(self.current_lang, {}).get(key, key)

    def change_language(self):
        """Allows user to change language anytime from settings."""
        print(self.t("settings_menu"))
        choice = input(self.t("select_lang")).strip()
        
        lang_map = {"1": "en", "2": "hi", "3": "mr"}
        if choice in lang_map:
            self.current_lang = lang_map[choice]
            print(f"\n✓ {self.t('lang_changed')}")
        else:
            print(f"\n⚠️ {self.t('invalid_choice')}")

    def display_dashboard(self):
        """Display health stats in the chosen language."""
        print("\n===============================")
        print(f"  {self.t('welcome')}")
        print("===============================")
        print(f"• {self.t('daily_goal')}")
        print(f"• {self.t('water_intake')}")

    def run(self):
        """Main application loop."""
        while True:
            choice = input(self.t("menu_prompt")).strip()
            
            if choice == "1":
                self.display_dashboard()
            elif choice == "2":
                self.change_language()
            elif choice == "3":
                print("\nGoodbye!")
                break
            else:
                print("Invalid option.")

# Launch App
if __name__ == "__main__":
    app = RillyApp()
    app.display_dashboard()
    app.run()