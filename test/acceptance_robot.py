
import rgkit.rg as rg


class Robot:
    def act(self, game):
        assert rg.CENTER_POINT is not None
        assert rg.locs_around((9, 9)) is not None
        return ['guard']
