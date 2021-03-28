from .. import _controllers as ctrl
from .._special import BSP, Buffer
from .._types import objects


class Scene:
    __slots__ = ('_bsp', '_scripts_md', '_objects', '_prefabs', '_update_queue', '_new_objects', '_del_queue')

    def __init__(self, init_data):
        config = ctrl.Config.instance()
        self._bsp = BSP(**config.get('defaultbsp'))
        self._scripts_md = ctrl.ModulesController.instance()
        self._prefabs = ctrl.PrefabsController.instance()
        self._objects = {}
        self._update_queue = Buffer(512)
        self._new_objects = Buffer(128)
        self._del_queue = Buffer(128)

        self._init(init_data)

    def _init(self, data) -> None:
        objects_data = data.get('objects', [])
        for i in objects_data:
            object_ = self.create_object(i['prefab'], i.get('params', {}))
            if isinstance(object_, objects.GameObject):
                tr = object_.transform
                for f, args in i.get('transform', {}).items():
                    getattr(tr, f)(*args)

    def _spawn_new(self):
        for object_ in self._new_objects.buffer():
            if isinstance(object_, objects.GameObject):
                self._update_queue.safe_push(object_)
            elif isinstance(object_, objects.DataObject):
                pass

    def _delete_objects(self):
        for id_ in self._del_queue.buffer():
            self._objects.pop(id_, None)

    def create_object(self, prefabname: str, params: dict):
        obj = self._prefabs.create(prefabname, params)
        if obj is not None:
            self._objects[obj.id] = obj
            self._new_objects.safe_push(obj)
        else:
            # TODO Предупреждение о несуществующем префабе
            pass
        return obj

    def destroy_object(self, id_: int):
        self._del_queue.safe_push(id_)

    def get_object_by_id(self, id_: int):
        return self._objects.get(id_)

    def update(self):
        self._delete_objects()
        self._spawn_new()
        current = self._update_queue.buffer()

        for obj in current:
            obj.update(0.02)
