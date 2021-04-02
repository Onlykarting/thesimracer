var progressBarValue = 100;
var progressBarsTime = setInterval(progressBars, 25 * document.getElementsByClassName('messages').length);

function progressBars() {
    if (progressBarValue < 0) {
        hider()
        clearInterval(progressBarsTime);
    } else {
        $('.progress-login').css({
            width: progressBarValue + '%'
        });

        $('.progress-register').css({
            width: progressBarValue + '%'
        });
        progressBarValue--;
    }
}

function hider() {
    $('.messages-block').hide(600, function () {
        $('.messages-block').remove();
    });
}

function choose_tab(a){
      document.getElementById(a).click();
}