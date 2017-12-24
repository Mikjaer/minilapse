<!DOCTYPE html>
<html>
<head>
	<title>Page Title</title>

	<meta name="viewport" content="width=device-width, initial-scale=1">

	<link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css" />
	<script src="http://code.jquery.com/jquery-2.2.4.min.js"></script>
	<script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
</head>
<body>

<div data-role="page">

	<div data-role="header">
		<h1>Mini Lapse ({if $status.running == "true"}running{else}standby{/if})</h1>

		<div data-role="navbar">
			<ul>
				<li><a href="?p=camera"{if $currentPage == "camera"} class="ui-btn-active"{/if} data-ajax="false">
					Camera</a></li>

				<li><a href="?p=files"{if $currentPage == "files"} class="ui-btn-active"{/if} data-ajax="false">
					Files</a></li>
			</ul>
		</div><!-- /navbar -->
	</div>

	<!-- /header -->


	<div role="main" class="ui-content">
		{$content}
	</div><!-- /content -->



	<div data-role="footer">
		<div data-role="navbar">
			<ul>
				<li><a href="?p=settings"{if $currentPage == "settings"} class="ui-btn-active"{/if} data-ajax="false">
					Settings</a></li>
				
				<li><a href="?p=wifi"{if $currentPage == "wifi"} class="ui-btn-active"{/if} data-ajax="false">
					Wifi</a></li>
				
				<li><a href="?p=bluetooth"{if $currentPage == "bluetooth"} class="ui-btn-active"{/if} data-ajax="false">
					Bluetooth</a></li>
			</ul>
		</div><!-- /navbar -->
		<h4>Mini Lapse ({if $status.running == "true"}running{else}standby{/if})</h4>
	</div><!-- /footer -->
</div><!-- /page -->

</body>
</html>
