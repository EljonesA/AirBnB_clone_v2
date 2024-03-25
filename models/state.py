#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel


class State(BaseModel):
    """ State class """
    name = ""

    def __init__(self, *args, **kwargs):
        ''' Initialize State class '''
        super().__init__(*args, **kwargs)

        if kwargs.get('name') is not None:
            self.name = kwargs['name']

    @property
    def cities(self):
        '''
        Getter method to return list of City objects linked to current State
        '''
        from models import storage
        from models.city import City

        city_objs = []
        all_cities = storage.all(City)
        for city_id, city in all.cities.items():
            if city.state_id == self.id:
                city_objs.append(city)
        return city_objs
