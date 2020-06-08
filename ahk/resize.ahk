CoordMode, Mouse, Screen
SysGet, BoundingCoordinates, MonitorWorkArea

ResolutionWidth := BoundingCoordinatesRight - BoundingCoordinatesLeft
ResolutionHeight := BoundingCoordinatesBottom - BoundingCoordinatesTop
;638,654
Send, {Esc}
Send, {LWin down}{Left down}{LWin up}{Left up}
MouseClick Left, 0.75 * ResolutionWidth, 0.5 * ResolutionHeight
MouseClick, Left, 484, 91
MouseClick Left, 0.75 * ResolutionWidth, 0.5 * ResolutionHeight
;MouseGetPos, xx, yy
;MouseMove, 0.5 * ResolutionWidth, 500
;if (A_Cursor == "SizeWE")
;    MouseClick, Left
;    MouseClickDrag, Left, 0.5 * ResolutionWidth, 0.5 * ResolutionWidth, 654, 500, 75
;MouseClick Left, 0.75 * ResolutionWidth, 0.5 * ResolutionHeight