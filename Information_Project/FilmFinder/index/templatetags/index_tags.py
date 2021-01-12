from django import template

register = template.Library()


@register.simple_tag
def get_avg_ratings(movie, banlist):
    return movie.average_rating(banlist)
