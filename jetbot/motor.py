# Written by SparkFun Electronics June 2019
# Author: Wes Furuya
# *Shell scripts were taken from original jetbot stats.py code.
#
# Do you like this code?
#
# Help support SparkFun and buy a SparkFun jetbot kit!
# https://www.sparkfun.com/products/15365
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------

import atexit
import traitlets
from traitlets.config.configurable import Configurable


class Motor(Configurable):

    value = traitlets.Float()

    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets

        self._driver = driver
        atexit.register(self._release)
        self.channel = channel

    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        """Sets motor value between [-1, 1]"""
        speed = int(255 * (self.alpha * value + self.beta))

	# Set Motor Controls: .set_drive( motor number, direction, speed)
	# Motor Number: A = 0, B = 1
	# Direction: FWD = 0, BACK = 1
	# Speed: (-255) - 255 (neg. values reverse direction of motor)

        if self.channel == 1:
            self._motor = self._driver.set_drive(self.channel-1, 0, speed)
        elif self.channel == 2:
            self._motor = self._driver.set_drive(self.channel-1, 0, speed)
        self._driver.enable()

    def _release(self):
        """Stops motor by releasing control"""
        self._driver.disable()
