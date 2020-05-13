from dataclasses import dataclass
from typing import List
from typing import Set

@dataclass
class Room:
    letter: str
    term: str
    last_updated: str
    
    def __hash__(self):
        return hash(self.letter)
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.letter == other.letter
        )

@dataclass
class Apartment:
    room_number: int
    capacity: int
    gender: str
    rooms: Set[Room]

    def __hash__(self):
        return hash(self.room_number)
    
    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.room_number == other.room_number
        )

@dataclass
class Building:
    id: int
    name: str
    apartments: Set[Apartment]
    restrictions: str
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and 
            self.id == other.id
        )

test_room = Room(letter="A", term="2020 Fall", last_updated="2020-04-22 08:02:09")

test_apartment = Apartment(room_number=219, capacity=6, gender="Male", rooms=[test_room])

test_building = Building(id=15, name="North Avenue North", apartments=[test_apartment], restrictions="Only 2nd years lel")

print(test_room)
print(test_apartment)
print(test_building)

print(test_building.apartments)

test_building_set = set([test_building])

test_building2 = Building(id=15, name="North Avenue North", apartments=[test_apartment], restrictions="Only 3nd years lel")

test_building_set.add(test_building2)

for building in test_building_set:
    print(building)




