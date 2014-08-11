<?php
	$db = mysqli_connect( "localhost","root","password","my_wiki" );
	if ( !$db ) {
		echo mysqli_connect_error();
		return;
	}

	$qstring = "SELECT wl_user, wl_namespace FROM watchlist;";
	$qresult = mysqli_query( $db, $qstring );

	$user = array();
	$user_wd = array();
	$user_wd_count = 0;
	$user_count = 0;

	while ( $row = mysqli_fetch_object( $qresult ) ) {
		$u = $row->wl_user;
		//check if the user is already counted as someone who watchlisted anything, if not, count it
		if ( !in_array( $u, $user ) ) {
			array_push($user, $u);
			$user_count++;
		}
		//check if the user is already counted as someone who watchlisted something in the namespace from 120 to 123, if not, count it
		if( !in_array($u, $user_wd) && $row->wl_namespace >= 120 && $row->wl_namespace <=123 ) {
			array_push($user_wd, $u);
			$user_wd_count++;
		}
	}

	echo "number of users, who watchlisted something in total: " .$user_count ."\n";
	echo "number of users, who watchlisted something in the namespace from 120 to 123: " .$user_wd_count ."\n";
?>
