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

	$currentstatus = $status = yaml_parse(file_get_contents("status.dat"));
	
	$stpl = new Mikjaer\SimpleTpl\SimpleTpl();

	$validPages = array("camera","files","settings","wifi","bluetooth");
	
	if (!in_array($_REQUEST["p"],$validPages))
		header("location: ?p=camera");
	$stpl->assign("currentPage", $currentPage=$_REQUEST["p"]);


	if ($currentPage == "camera")
	{
		if ($_REQUEST["a"] == "start")
			$status["running"] = "true";
	
		if ($_REQUEST["a"] == "stop")
			$status["running"] = "false";

		if ($_REQUEST["a"] == "update")
			die(header("location: ?p=camera"));
	}

	if ($currentPage == "files")
	{
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
