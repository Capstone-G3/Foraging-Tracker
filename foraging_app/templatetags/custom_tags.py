from django import template

register = template.Library()

@register.simple_tag
def get_first_species(species_list, category):
    for species in species_list:
        if species.category == category:
            return species
    return None
