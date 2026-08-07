class ThemeManager:
    def __init__(self):
        self.theme = "light"
        self.bg_color = "white"
        self.fg_color = "black"

    def toggle(self):
        if self.theme == "light":
            self.theme = "dark"
            self.bg_color = "black"
            self.fg_color = "white"
        else:
            self.theme = "light"
            self.bg_color = "white"
            self.fg_color = "black"

# Example usage:
app_theme = ThemeManager()

app_theme.toggle()
print(f"Theme: {app_theme.theme}, Background: {app_theme.bg_color}")
# Output: Theme: dark, Background: black

app_theme.toggle()
print(f"Theme: {app_theme.theme}, Background: {app_theme.bg_color}")
# Output: Theme: light, Background: white



# End of file
