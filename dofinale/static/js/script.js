/* Custom JS Script */

// 비디오 여러 개 재생 jquery. 바닐라 스크립트로 변환 시도해봐야 함.
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