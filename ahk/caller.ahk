#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.

If (%0% < 1)
{
    MsgBox, No number was provided!
}
Else
{
    SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
    SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory
    ;CmdLine := DllCall("GetCommandLine", "Str"])
    ;pArgs := DllCall( "Shell32\CommandLineToArgvW", "WStr",CmdLine, "PtrP",nArgs, "Ptr" )
    CoordMode, Mouse, Screen
    ;#MouseMove, X, Y [, Speed, Relative]
    ;416, 261
    MouseMove, 240, 197, 50
    MouseClick, Left ;[, X, Y, ClickCount, Speed, D|U, R]
    Sleep, 1000
    Send, %1%
    Sleep, 1000
    Send, {Enter}
}
ExitApp, 0