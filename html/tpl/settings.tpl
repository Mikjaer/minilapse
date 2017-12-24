<form method="post">
	<label for="text-basic">Projectname (10 Alphanumeric):</label>
	<input type="text" name="text-basic" id="text-basic" value="{$status.projectname}">

	<label for="select-choice-1" class="select">Framerate:</label>
	<select name="select-choice-1" id="select-choice-1">
    		<option value="standard">60 Frames pr minute</option>
    		<option value="standard">30 Frames pr minute</option>
    		<option value="standard">15 Frames pr minute</option>
    		<option value="standard">1 Frame pr minute</option>
    		<option value="standard">30 Frames pr hour</option>
    		<option value="standard">15 Frames pr hour</option>
    		<option value="standard">1 Frame pr hour</option>
	</select>

	<button class="ui-shadow ui-btn ui-corner-all">Perform changes</button>

</form>
