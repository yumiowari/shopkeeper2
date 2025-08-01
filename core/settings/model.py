class Model:
    def __init__(self):
        pass

    def update_curr_theme(self, theme_name):
        with open('data/curr_theme.txt', 'w') as f:
            f.write(theme_name)