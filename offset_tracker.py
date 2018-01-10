class OffsetTracker:
    def __init__(self, starting_offset=0):
        self._offset = starting_offset

    @property
    def offset(self):
        return self._offset


    @offset.setter
    def offset(self, new_offset):
        if new_offset < 0:
            self._offset = 0
        else:
            self._offset = new_offset

    def reset(self):
        self._offset = 0
