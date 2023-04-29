from CaptionGen import CaptionGen
import random

### These are alternative (unused) templates for generating captions.
### The only function used in the final version of TraVLR is gen_caption_exact.
SPATIAL_DATASET_TEMPLATE = "SpatialDatasetGen/captions.txt"
SPATIAL_DATASET_TEMPLATE_2 = "SpatialDatasetGen/captions2.txt"

class SpatialCaptionGen(CaptionGen):
    def __init__(self, object_list, relationship, settings):
        self.object_list = object_list
        self.relationship = relationship
        self.settings = settings

    def gen_caption_exact(self, train, caption_abstract=None):
        '''
        Returns a single caption/description of the condition. 
        '''
        caption, caption_abstract = self.gen_caption_obj_list_exists(
            self.object_list, train=train, caption_abstract=caption_abstract)
        caption = '{} {}'.format(self.gen_prompt(
            self.settings.num_rows), caption)
        return [{
            "caption": caption,
            "caption_abstract": caption_abstract
        }]
    
    def gen_captions(self):
        """
        Returns all possible true descriptions of a condition (represented by an object list), given a relationship. 
        If there are 2 objects, there are 2 captions returned (e.g. "A is to the left of B."/"B is to the right of A")
        If there are 3 objects, there are 3 captions returned.
        """
        captions = []
        templates = self.read_templates(SPATIAL_DATASET_TEMPLATE)
        template = templates[0] if self.settings.single_template else random.choice(
            templates)
        first_rel, second_rel = self.get_rel(self.relationship)

        pairs = []
        for idx in range(len(self.object_list)-1):
            pairs.append([self.object_list[idx], self.object_list[idx+1]])

        caption_pairs = list(map(lambda p: [self.gen_caption_two_objs(template, p[0], p[1], first_rel),
                                            self.gen_caption_two_objs(template, p[1], p[0], second_rel)], pairs))

        if self.settings.num_objs == 2:
            return list(enumerate(caption_pairs[0]))
        elif self.settings.num_objs == 3:
            for cpt1 in caption_pairs[0]:
                for cpt2 in caption_pairs[1]:
                    captions.append("{first} {second}".format(
                        first=cpt1, second=cpt2))
            return list(enumerate(captions))

    def gen_caption_from_template(self, train, template_file=SPATIAL_DATASET_TEMPLATE_2):
        '''
        Returns a single caption/description of the condition. 
        The template is randomly selected from the provided template list.
        '''
        captions = []
        templates = self.read_templates(template_file)
        template = templates[0] if self.settings.single_template else random.choice(
            templates)
        captions.append(self.gen_caption_obj_list(
            template, self.object_list, None, train=train))
        return list(enumerate(captions))
