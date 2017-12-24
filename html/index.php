<?php
	include("./SimpleTpl/src/SimpleTpl.php");

	function sizify($size)
	{
		if (($size + 1) > 1024 * 1024 * 1024)
			return sprintf("%.2f GiB",$size / 1024 / 1024 / 1024);
		if (($size + 1) > 1024 * 1024)
			return sprintf("%.2f MiB",$size / 1024 / 1024);
	
		if (($size + 1) > 1024)
			return sprintf("%.2f KiB",$size / 1024);
		return $size;
	}


	function sendCommand($command)
	{
		$service_port = "1337";
		$address = "127.0.0.1";

		$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($socket === false) {
			    echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
		}

		$result = socket_connect($socket, $address, $service_port);
		if ($result === false) {
		    echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
		} 

		$in = $command."\r\n";
		socket_write($socket, $in, strlen($in));

		$in = "QUIT\r\n";
		socket_write($socket, $in, strlen($in));

		while ($out = socket_read($socket, 2048)) {
			// Waiting for connection to be terminated
		}

		socket_close($socket);
	}

	$currentstatus = $status = yaml_parse(file_get_contents("status.dat"));
	
	$stpl = new Mikjaer\SimpleTpl\SimpleTpl();

	$validPages = array("camera","files","settings","wifi","bluetooth");
	

	if (isset($_REQUEST["ajax"]))
	{
		switch ($_REQUEST["ajax"])
		{
			case "preview":
				sendCommand("PREVIEW");
				print json_encode("/preview.jpg?".time());
				die();
		}
	}

	if (!in_array($_REQUEST["p"],$validPages))
		header("location: ?p=camera");
	$stpl->assign("currentPage", $currentPage=$_REQUEST["p"]);

	if ($currentPage == "camera")
	{
		if (isset($_REQUEST["a"]))
		{
			if ($_REQUEST["a"] == "start")
				$status["running"] = "true";
	
			if ($_REQUEST["a"] == "stop")
				$status["running"] = "false";

			if ($_REQUEST["a"] == "update")
				die(header("location: ?p=camera"));
		}	
	}

	if ($currentPage == "files")
	{
		if (isset($_REQUEST["a"]))
			if ($_REQUEST["a"] == "delete")
			{
				system("rm ".$status["storagePath"]."/".$_REQUEST["file"]);
			}
		$dir = opendir($path=($status["storagePath"]));
		while ($dat = readdir($dir))
			if (is_file($path."/".$dat))
				$files[] = $dat;

		sort($files);

		foreach ($files as $file)
		{
			$stpl->append("files",array(
				"name" => $file,
				"size" => sizify(filesize($path."/".$file))
			));
		}

	}


	$stpl->assign("status",$status);
	$stpl->assign("content", $stpl->fetch("tpl/$currentPage.tpl"));



	$stpl->display("tpl/main.tpl");

#	if ($currentstatus != $status)
		file_put_contents("status.dat",yaml_emit($status));
