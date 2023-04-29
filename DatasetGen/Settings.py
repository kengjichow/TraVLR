class Settings:
    def __init__(self, num_rows, num_cols, num_objs, num_test_objs=None, single_template=True):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_objs = num_objs
        self.num_test_objs = num_test_objs
        self.single_template = single_template
        self.image_height = 500
        self.image_width = 500