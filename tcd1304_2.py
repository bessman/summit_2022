import matplotlib.pyplot as plt

from pslab.instrument.oscilloscope import Oscilloscope
from pslab.instrument.waveform_generator import PWMGenerator
from pslab.serial_handler import SerialHandler


class TCD1304:
    def __init__(self, device: SerialHandler):
        self._pwm = PWMGenerator(device)
        self._scope = Oscilloscope(device)
        self._sh_frequency = 125

    def start_clocks(self):
        self._pwm.map_reference_clock(channels="SQ1", prescaler=6)
        self._pwm.generate(
            channels=["SQ2", "SQ3"],
            frequency=self._sh_frequency,
            duty_cycles=[
                1e-6 / self._sh_frequency**-1,
                1 - 2.5e-6 / self._sh_frequency**-1,
            ],
            phases=[1 - 2.5e-6 / self._sh_frequency**-1, 0],
        )

    def read(self):
        return self._scope.capture(
            channels="CH3",
            samples=4000,
            timegap=2,
            trigger=3,
            trigger_channel="CH2",
        )


if __name__ == "__main__":
    device = SerialHandler()
    tcd = TCD1304(device)
    tcd.start_clocks()
    x, y = tcd.read()
    (ax,) = plt.plot(x, y)
    for _ in range(100):
        x, y = tcd.read()
        ax.set_ydata(y)
        plt.pause(0.05)
