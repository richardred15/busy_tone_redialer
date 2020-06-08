CoordMode, Mouse, Screen
SetTimer, Check, 20
return
;640,654
Check:
MouseGetPos, xx, yy
ToolTip, %xx%`, %yy%`, %1%
return

Esc::ExitApp