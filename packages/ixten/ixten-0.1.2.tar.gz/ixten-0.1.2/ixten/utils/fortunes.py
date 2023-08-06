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

import random


MESSAGES = [
    "-- We are CCSI! --",
    "-- No habrá paz para los malvados --",
    "-- If it's there, we will find it! --",
    "-- Knock, knock! --",
    "-- Is anybody alive out there? --",
    "-- Llaman a la puerta… --",
    "-- ¿Quién será, será? --",
]


def get_message():
    """Gets a random fortune

    Returns:
        str. A random fortune"""
    return random.choice(MESSAGES)
