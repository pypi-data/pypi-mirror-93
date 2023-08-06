# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  Copyright (C) 2019-2020
#   Laboratory of Systems Biology, Department of Cybernetics,
#   School of Science, Tallinn University of Technology
#  This file is part of project: IOCBIO Kinetics
#
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSplashScreen

class SmallLabel(QLabel):
    """Shows a label in small font"""
    
    def __init__(self, text, word_wrap=True):
        QLabel.__init__(self, '<small>'+text+'</small>')
        self.setWordWrap(word_wrap)

        
class SplashScreen(QSplashScreen):

    def __init__(self, pixmap):
        QSplashScreen.__init__(self, pixmap)

    def showMessage(self, message):
        QSplashScreen.showMessage(self, message, Qt.AlignBottom | Qt.AlignCenter, Qt.black)
        
