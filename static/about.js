var didScroll;
var lastScrollTop = 0;
var delta = 5;
var navbarHeight = $('#navbar').outerHeight();
$(window).scroll(function(event){
    didScroll = true;
});

setInterval(function() {
    if (didScroll) {
        hasScrolled();
        didScroll = false;
    }
}, 250);

function hasScrolled() {
    var st = $(this).scrollTop();
    

    if(Math.abs(lastScrollTop - st) <= delta)
        return;
    

    if (st > lastScrollTop && st > navbarHeight){
       
        $('#navbar').css('top','-60px');
    } else {
       
        if(st + $(window).height() < $(document).height()) {
            $('#navbar').css('top','0');
        }
    }
    
    lastScrollTop = st;
}