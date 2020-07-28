window.onload = function() {
	var startDate = startDateHtml
	var nowDate = new Date();
	var timeDifference;

	if (startDate) {
	  startDate = new Date(startDate);
	}
	timeDifference = ( startDate.getTime() - nowDate.getTime() )

	if (timeDifference > 0) {
		setTimeout( function() {
		  location.reload(true)
		}, timeDifference );
	}
};