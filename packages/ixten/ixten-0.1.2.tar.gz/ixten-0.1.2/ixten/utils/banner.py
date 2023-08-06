################################################################################
#    Copyright 2021 @ Telefónica
#
#    This program is part of Ixten. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


import ixten.utils.misc as misc
import ixten.utils.fortunes as fortunes


def show_banner():
    welcome = misc.title("""
                        ___      _
                       |_ _|_  _| |_ ___ _ __
                        | |\ \/ / __/ _ \ '_ \  
                        | | >  <| ||  __/ | | |
                       |___/_/\_\\\__\___|_| |_|

    """) + f"""

                      Coded with {misc.error('♥')} @ {misc.success('Telefónica')}

{misc.warning(fortunes.get_message()).center(80)}

    """
    print(welcome)
