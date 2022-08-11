/* Custom JS Script */

//
$(function(){
    $("#video1").bind("ended", function() {
        window.getElementById("video2").play();
 	});
	$("#video2").bind("ended", function() {
        window.getElementById("video3").play();
    });
	$("#video3").bind("ended", function() {
 		window.getElementById("video1").play();
 	});
});