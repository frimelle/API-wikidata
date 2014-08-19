<?php
/**
 * This script is supposed to connect with a wikibase database to check how many users have Wikibase/Wikidata changes in their watchlist enabled, 
 * how many users see wikibase/wikidata in their recent changes and
 * how many users have enhanced recent changes enabled. 
**/
	$db = mysqli_connect( "localhost","root","password","my_wiki" );
	if ( !$db ) {
		echo mysqli_connect_error();
		return;
	}
	$month = 3;
	$qstring_wl = "SELECT DISTINCT up_user FROM user_properties INNER JOIN recentchanges ON rc_user = up_user WHERE up_property = 'wlshowwikibase' AND rc_timestamp >= ( now() - INTERVAL " .$month ." MONTH);";
	$qstring_rc = "SELECT DISTINCT up_user FROM user_properties INNER JOIN recentchanges ON rc_user = up_user WHERE up_property = 'rcshowwikidata' AND rc_timestamp >= ( now() - INTERVAL " .$month ." MONTH);";
	$qstring_urc = "SELECT DISTINCT up_user FROM user_properties INNER JOiN recentchanges ON rc_user = up_user WHERE up_property = 'usenewrc' AND rc_timestamp >= ( now() - INTERVAL " .$month ." MONTH);";
	
	$qresult_wl = mysqli_query( $db, $qstring_wl );
	$qresult_rc = mysqli_query( $db, $qstring_rc );
	$qresult_urc = mysqli_query( $db, $qstring_urc );

	$wl_wb_user = 0;
	while ( $row_wl = mysqli_fetch_object( $qresult_wl ) ) {
		$wl_wb_user++;
	}

	$rc_wb_user = 0;
	while ( $row_rc = mysqli_fetch_object( $qresult_rc ) ) {
		$rc_wb_user++;
	}

	$use_rc_user = 0;
	while ( $row_urc = mysqli_fetch_object( $qresult_urc ) ) {
		$use_rc_user++;
	}


	echo "wlshowwikibase: " .$wl_wb_user ."\n";
	echo "rcshowwikidata: " .$rc_wb_user ."\n";
	echo "usenewrc: " .$use_rc_user ."\n";
?>