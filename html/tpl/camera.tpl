<img id=preview src="preview.jpg" style="width: 90%; margin-left: 5%;">
<script>
function updatepreview()
{

	$.mobile.loading( "show", {
  		textVisible: true,
  		theme: "a",
  		html: "",
		text: "Taking picture"
	});	

	$.getJSON("/index.php?ajax=preview", function (data) {
		$("#preview").attr("src",data);
		$.mobile.loading ("hide");
	});	


}
</script>
<p>
<div class="ui-grid-b">

	<div class="ui-block-a"> <a href="?p=camera&a=start" class="ui-shadow ui-btn ui-corner-all{if $status.running == "true"} ui-state-disabled{/if}">Start</a></div>

	<div class="ui-block-b"> <a href="?p=camera&a=stop" onclick="return confirm('Do you realy wish to stop timelapse?');" class="ui-shadow ui-btn ui-corner-all{if $status.running == "false"} ui-state-disabled{/if}">Stop</a></div>
	<div class="ui-block-c"> <a href="javascript: updatepreview();" class="ui-shadow ui-btn ui-corner-all{if $status.running == "true"} ui-state-disabled{/if}" data-ajax="false">Update</a></div>
</div>

<ul data-role="listview" data-count-theme="a" data-inset="true">
	<li>Time Lapse Status:<span class="ui-li-count">
		{if $status.running == "true"}
			running
		{else}
			standby
		{/if}
	</span></li>
	<li>Running since:<span class="ui-li-count">12:01</span></li>
	<li>Storage usage:<span class="ui-li-count">25%</span></li>
	<li>Time left:<span class="ui-li-count">12 hours 12 min</span></li>
</ul>

</p>
