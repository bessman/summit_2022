import matplotlib.pyplot as plt

from pslab.instrument.logic_analyzer import LogicAnalyzer
from pslab.instrument.waveform_generator import PWMGenerator
from pslab.serial_handler import SerialHandler


class TCD1304:
    def __init__(self, device: SerialHandler):
        self._pwm = PWMGenerator(device)
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


if __name__ == "__main__":
    device = SerialHandler()
    la = LogicAnalyzer(device)
    tcd = TCD1304(device)
    tcd.start_clocks()
    t = la.capture(channels=2, events=2)
    x1, y1, x2, y2 = la.get_xy(t)
    plt.plot(x1, y1, x2, y2 + 1.1)
