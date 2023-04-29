from CaptionGen import CaptionGen
import random


class CompareCaptionGen(CaptionGen):
    def __init__(self, object_list, settings):
        self.object_list = object_list
        self.settings = settings

    def gen_captions(self):
        '''
        Returns a single caption/description of the condition. 
        The template is randomly selected from the provided template list.
        '''
        captions = []
        objects_dict = self.get_objects_dict()
        caption = self.gen_caption_without_position(objects_dict)
        captions.append(caption)
        return captions

    def gen_caption_exact(self, train, caption_abstract=None):
        '''
        Returns a single caption/description of the condition. 
        '''
        caption, caption_abstract = self.gen_caption_obj_list_exists(
            self.object_list, train=train, caption_abstract=caption_abstract)
        caption = '{} {}'.format(self.gen_prompt(self.settings.num_rows), caption)
        return [{
            "caption": caption,
            "caption_abstract": caption_abstract
        }]
