# OverwatchRoleSelector
A way to randomly assign a group of players overwatch roles.


![image](https://user-images.githubusercontent.com/43573052/217600906-86f81a03-4df6-4b96-b7d5-e61f5a5e0110.png)

<ins>**keybindings:<br />**</ins>
**Up/Down arrow keys:** Navigate up and down in the currently selected list.<br />
**Right/D:** Move The player currently selected in the 'available' list to the 'selected' list.<br />
**Left/A:** Move The player currently selected in the 'selected' list to the 'available' list.<br />
**Ctrl:** Swap currently focused list.<br />
**1,2,3,4,5:** Toggle the roles that players can be assigned to.<br />
**Space/Return:** Roll the selector.<br />

<ins>**Edit player names:<br />**</ins>
To edit the players in the available list simply edit the 'players.txt' file in the same directory<br />
as the 'RoleSelector.py'. Place each player name on a newline, save the file and then relaunch the program.<br />
<br />
<ins>**How to use:<br />**</ins>
Move the players you wish to select from the 'available' list into the 'selected' list.<br />
click the player name in the list then the arrow buttons or use the arrow keys and ctrl.<br />
<br />
Once you have your player list ready, select which roles you wish to assign using the checkboxes on the right<br />
or use the numbers 1 to 5 to select them respectively.
<br />
Once you have both the players and rolls selected, press the roll button and the players will be assigned randomly<br />
to their roles at the bottom of the window. Any errors in this process will be displayed at the bottom in the grey.

<ins>**How to Run:<br />**</ins>
This program requires at least python 3.7 to run. Simply double click the 'RoleSelector.py' file with python 
installed to launch.<br />
May not function correctly on versions of python with older tcl-tk versions on mac and linux