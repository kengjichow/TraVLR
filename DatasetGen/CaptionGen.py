import random

class CaptionGen:
    def read_templates(self, filename):
        templates = []
        with open(filename, 'r') as reader:
            templates += (reader.readlines())
        return templates

    def gen_caption_two_objs(self, template, obj1, obj2, rel):
        template = template.split()
        result = []
        for w in template:
            if w == "{obj1.colour}":
                result.append(obj1.colour.value)
            elif w == "{obj1.shape}":
                result.append(obj1.shape.value)
            elif w == "{obj2.colour}":
                result.append(obj2.colour.value)
            elif w == "{obj2.shape}":
                result.append(obj2.shape.value)
            elif w == "{rel}":
                result.append(rel)
            elif w == "{obj1.position}":
                result.append(self.gen_chess_coord(obj1))
            elif w == "{obj2.position}":
                result.append(self.gen_chess_coord(obj2))
            else:
                result.append(w)
        result = " ".join(result) + "."
        return result

    def gen_prompt(self, grid_size="6"):
        prompt_6x6 = "The left-most column is A, the right-most column is F, the top-most row is 1, and the bottom-most row is 6."
        prompt_10x10 = "The left-most column is A, the right-most column is J, the top-most row is 1, and the bottom-most row is 10."

        prompt_6x6 = "Columns, left to right, are ordered A to F. Rows, top to bottom, are ordered 1 to 6."
        prompt_10x10 = "Columns, left to right, are ordered A to J. Rows, top to bottom, are ordered 1 to 10."
        if grid_size == 6:
            prompt = prompt_6x6
        elif grid_size == 10:
            prompt = prompt_10x10
        return prompt

    def gen_caption_obj_list_exists(self, obj_list, train, caption_abstract=None):
        '''
        Generates caption: "There is an orange square at A2, a red circle at B1, etc..."
        '''
        if caption_abstract is not None:
            obj_list = list(map(lambda x: obj_list[x], caption_abstract))
        else:
            obj_list = random.sample(obj_list, len(obj_list))
        result = []
        abstract = []
        for i in range(len(obj_list)):
            abstract.append(obj_list.index(obj_list[i]))
            result.append("{article} {colour} {shape} at {position}".format(
                    article="an" if obj_list[i].colour.value[0] in ["a", "e", "i", "o", "u"] else "a",
                    colour=obj_list[i].colour.value,
                    shape=obj_list[i].shape.value,
                    position=self.gen_chess_coord(obj_list[i], train)))
        result = "There is " + ", ".join(result[:-1]) + " and " + result[-1] + "."
        result = result[:1].upper() + result[1:]
        return result, abstract

    def gen_caption_obj_list(self, obj_list, train):
        shuffled = random.sample(obj_list, len(obj_list))
        result = []
        abstract = []
        for i in range(len(shuffled)):
            abstract.append(obj_list.index(shuffled[i]))
            result.append("the {colour} {shape} is at {position}".format(
                    colour=shuffled[i].colour.value,
                    shape=shuffled[i].shape.value,
                    position=self.gen_chess_coord(shuffled[i], train)))
        result = ", ".join(result[:-1]) + " and " + result[-1] + "."
        result = result[:1].upper() + result[1:]
        return result, abstract

    def gen_caption_obj_list_from_template(self, template, obj_list, rel, train):
        '''
        Generate chessboard caption from pre-defined template
        '''
        template = template.split()
        result = []
        for w in template:
            if w == "{obj1.colour}":
                result.append(obj_list[0].colour.value)
            elif w == "{obj1.shape}":
                result.append(obj_list[0].shape.value)
            elif w == "{obj2.colour}":
                result.append(obj_list[1].colour.value)
            elif w == "{obj2.shape}":
                result.append(obj_list[1].shape.value)
            elif w == "{obj3.colour}":
                result.append(obj_list[2].colour.value)
            elif w == "{obj3.shape}":
                result.append(obj_list[2].shape.value)
            elif w == "{rel}":
                result.append(rel)
            elif w == "{obj1.position}":
                result.append(self.gen_chess_coord(obj_list[0], train))
            elif w == "{obj2.position}":
                result.append(self.gen_chess_coord(obj_list[1], train))
            elif w == "{obj3.position}":
                result.append(self.gen_chess_coord(obj_list[2], train))
            else:
                result.append(w)
        result = " ".join(result) + "."
        result = self.gen_preface(train) + result
        return result

    def gen_preface(self, train):
        if train:
            return "Left to right is A to Z and top to bottom is 1 to 10. "
        else:
            return "Left to right is Z to A and top to bottom is 10 to 1. "

    def gen_chess_coord(self, obj, train):
        return self.get_actual_chess_coord(obj)

    def get_actual_chess_coord(self, obj):
        col_dict = {
            0: "A",
            1: "B",
            2: "C",
            3: 'D',
            4: 'E',
            5: 'F',
            6: 'G',
            7: 'H',
            8: 'I',
            9: 'J'
        }
        row_dict = { i: str(i+1) for i in range(0, 10)}
        return col_dict[obj.column] + " " + row_dict[obj.row]

    def get_random_coord(self, obj):
        col_dict = {
            0: "C",
            1: "J",
            2: "I",
            3: 'E',
            4: 'H',
            5: 'A',
            6: 'F',
            7: 'B',
            8: 'D',
            9: 'G'
        }
        row_dict = {
            0: "6",
            1: "3",
            2: "7",
            3: '1',
            4: '10',
            5: '2',
            6: '9',
            7: '8',
            8: '4',
            9: '5'
        }
        return col_dict[obj.column] + " " + row_dict[obj.row]

    def get_reversed_coord(self, obj):
        col_dict = {
            0: "J",
            1: "I",
            2: "H",
            3: 'G',
            4: 'F',
            5: 'E',
            6: 'D',
            7: 'C',
            8: 'B',
            9: 'A'
        }
        row_dict = { (10-i): str(i) for i in range(10, 0, -1)}
        return col_dict[obj.column] + " " + row_dict[obj.row]

    def gen_caption_without_position(self, objects_dict):
        caption = "There are"
        if len(objects_dict) == 0:
            return "There are no objects."
        for obj in objects_dict:
            caption += " {number} {colour} {shape}s,".format(number=objects_dict[obj], colour=obj.colour.value, shape=obj.shape.value)
        caption = caption[:-1] + "."
        return caption

    def get_objects_dict(self):
        dic = {}
        for obj in self.object_list:
            found = False
            for key in dic:
                if key.sameAttr(obj):
                    dic[key] += 1
                    found = True
                    break
            if not found:
                dic[obj] = 1
        return dic

    def gen_caption_without_position_unnumbered(self, objects):
        caption = "There is"
        if len(objects) == 0:
            return "There are no objects."
        for obj in objects:
            caption += " a {colour} {shape},".format(colour=obj.colour.value, shape=obj.shape.value)
        caption = caption[:-1] + "."
        return caption

    def get_number_word(self, number):
        dic = {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine'
        }
        return dic[number]