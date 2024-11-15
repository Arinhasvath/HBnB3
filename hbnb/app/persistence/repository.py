from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self, model_class=None):
        self._storage = {}
        self.model_class = model_class

    def add(self, obj):
        print(f"Ajout de l'objet {obj.id} : {obj}")
        self._storage[obj.id] = obj

    def get(self, obj_id):
        obj = self._storage.get(obj_id)
        print(f"Récupération de l'objet {obj_id} : {obj}")
        return obj

    def get_all(self):
        print(f"Récupération de tous les objets")
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            print(f"Mise à jour de l'objet {obj_id} : {obj}")
        else:
            raise ValueError(f"Object with ID {obj_id} not found")

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            print(f"Suppression de l'objet {obj_id}")
        else:
            raise ValueError(f"Object with ID {obj_id} not found")

    def get_by_attribute(self, attr_name, attr_value):
        print(f"Récupération de l'objet avec {attr_name} = {attr_value}")
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

