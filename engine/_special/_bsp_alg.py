class NodeRect:
    __slots__ = ('size', '_xmin', '_ymin', '_xmax', '_ymax')

    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float):
        self.size = xmax - xmin
        self._xmin = xmin
        self._ymin = ymin
        self._xmax = xmax
        self._ymax = ymax

    def contain(self, xmin: float, ymin: float, xmax: float, ymax: float) -> bool:
        return self._xmin < xmin < xmax < self._xmax and \
               self._ymin < ymin < ymax < self._ymax

    def collide(self, xmin: float, ymin: float, xmax: float, ymax: float) -> bool:
        return (xmax - xmin + self.size) / 2 > max(abs(self._xmin - xmax), abs(self._xmax - xmin)) and \
               (ymax - ymin + self.size) / 2 > max(abs(self._ymin - xmax), abs(self._ymax - xmin))


class Node(NodeRect):
    __slots__ = ('childs', 'outdated', 'objects')

    def __init__(self, xmin: float, ymin: float, xmax: float, ymax: float):
        super().__init__(xmin, ymin, xmax, ymax)
        self.childs = []
        self.objects = []
        self.outdated = False

    def _sieve_all(self):
        for c in self.childs:
            for o in self.objects:
                c.sieve(o, check=True)
        del self.objects

    def reset(self):
        self.outdated = False
        if self.childs:
            for i in self.childs:
                i.reset_flag = True
        else:
            cl = self.collide
            self.objects = [o for o in self.objects if cl(*o.transform.boundary())]

    def division(self) -> None:
        x, y, w = self._xmin, self._ymin, self.size / 2
        points = [(x, y), (x + w, y), (x, y + w), (x + w, y + w)]
        self.childs = [Node(nx, ny, nx + w, ny + w) for nx, ny in points]
        self._sieve_all()

    def sieve(self, object_, check=False) -> None:
        if check and not self.collide(*object_.transform.boundary()):
            return
        self.objects.append(object_)


class BSP:
    __slots__ = ('_min_size', '_objlim', '_root', '_cache')

    def __init__(self,
                 initsize=65536,
                 minsize=2,
                 objectslimit=7):
        self._min_size = minsize
        self._objlim = objectslimit

        initsize /= 2
        self._root = Node(-initsize, -initsize, initsize, initsize)
        self._cache = {}

    def _check_cache(self, object_):
        cached = self._cache.get(object_.id)
        if cached is not None:
            if cached.contain(*object_.transform.boundary()):
                return True
            self._cache.pop(object_.id)
        return False

    def _update_node(self, node: Node) -> None:
        if node.outdated:
            node.reset()
        if len(node.objects) > self._objlim and node.size / 2 > self._min_size:
            node.division()

    def _sieve(self, object_):
        stack, update, cache = [self._root], self._update_node, self._cache
        xmin, ymin, xmax, ymax = object_.transform.boundary()

        while stack:
            node = stack.pop()
            update(node)
            if node.childs:
                stack.extend(n for n in node.childs if n.collide(xmin, ymin, xmax, ymax))
            else:
                node.sieve(object_)
                if node.contain(xmin, ymin, xmax, ymax):
                    cache[object_.id] = node
                    break

    def reset(self):
        self._root.outdated = True

    def sieve(self, object_):
        if not self._check_cache(object_):
            self._sieve(object_)

    def scan(self, xmin, ymin, xmax, ymax) -> list:
        stack, update = [self._root], self._update_node
        tmp_node = NodeRect(xmin, ymin, xmax, ymax)
        scanned = set()
        ans = []

        while stack:
            node = stack.pop()
            update(node)
            if node.childs:
                stack.extend(n for n in node.childs if n.collide(xmin, ymin, xmax, ymax))
            else:
                cur = {o for o in node.objects if tmp_node.collide(*o.transform.boundary() and o not in scanned)}
                scanned.update(cur)
                ans.extend(cur)

        return ans
