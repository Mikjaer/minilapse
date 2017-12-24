
<div data-role="collapsibleset" data-count-theme="b" data-inset="true">

{foreach name=loop loop=$files}
	<div data-role="collapsible" data-collapsed-icon="carat-r">
	<h2>{$files[loop.index].name}<span class="ui-li-count">{$files[loop.index].size}</span></h2>

	<div class="ui-grid-b">


		
		<div class="ui-block-a"> <a href="?p=files&a=delete&file={$files[loop.index].name}" onclick="return confirm('Do you realy wish to delete this file?');" class="ui-shadow ui-btn ui-corner-all">Delete</a></div>
		
	
		<div class="ui-block-b"> <a href="?p=camera&a=update&files={$files[loop.index].name}" class="ui-shadow ui-btn ui-corner-all{if $status.bluetooth != "true"} ui-state-disabled{/if}" data-ajax="false">Upload</a></div>
		
		<div class="ui-block-c"> <a href="{$status.storageUrl}/{$files[loop.index].name}" class="ui-shadow ui-btn ui-corner-all" data-ajax="false">Download</a></div>
	</div>
	</div>
{/foreach}
</div>
