import base64
import io

from matplotlib import interactive
from matplotlib.backend_bases import FigureManagerBase, _Backend
from matplotlib.backends import backend_agg

interactive(True)


class FigureCanvasAggBase64(backend_agg.FigureCanvasAgg):
    """
    A canvas backend that captures the figure as a Base64 PNG string.
    """

    def draw(self):
        # Render the figure to a PNG in memory
        buf = io.BytesIO()
        # Use the figure's DPI for consistency
        self.figure.savefig(buf, format="png")
        buf.seek(0)
        # Encode and store in the global variable
        rendered = "base64," + base64.b64encode(buf.read()).decode("utf-8")
        # Close the buffer
        buf.close()
        # Clear the figure to free up memory
        self.figure.clf()
        # Return the Base64 string
        return rendered


class FigureManagerAggBase64(FigureManagerBase):
    def __init__(self, canvas, num):
        super().__init__(canvas, num)
        self.set_window_title(f"Figure {num}")

    def show(self, *args, **kwargs):
        # Trigger the draw to update `rendered`
        return self.canvas.draw()

    def destroy(self, *args, **kwargs):
        # No resources to clean up
        pass


@_Backend.export
class _BackendBase64(_Backend):
    """
    Exported backend that produces a Base64 PNG string.
    """

    FigureCanvas = FigureCanvasAggBase64
    FigureManager = FigureManagerAggBase64

    @staticmethod
    def show(*args, **kwargs):
        from matplotlib import pyplot as plt

        return plt.gcf().canvas.draw()

    @staticmethod
    def destroy(*args, **kwargs):
        from matplotlib import pyplot as plt

        # No-op for destruction
        pass
