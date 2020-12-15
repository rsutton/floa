"use strict";
$(document).ready(function(){
    let $SCRIPT_ROOT = location.origin;
    let status_icons = ['fa-circle-o', 'fa-check', 'fa-heart']

    // initialize home view
    let activePage = $('.nav-link active').text()
    showBookshelf();

    // handle checkbox status
    function iconClassMatcher(index, className){
        let matchedClasses = className.match(/(^|\s)fa-\S+/g)
        return (matchedClasses || []).join('')
    }
    // initialize status
    $( '.content-listing' ).each(function(){
        let status = $(this).attr('data-status')
        $(this).children('.content-listing__control').removeClass(iconClassMatcher).addClass(status_icons[status]);
    });

    // tri-state checkbox click handler
    $( '.content-listing__control' ).click(function(){
        let current_status = $(this).parent().attr('data-status');
        let new_status = (current_status + 1) % status_icons.length;
        $(this).parent().attr('data-status', new_status);
        $(this).removeClass(iconClassMatcher).addClass(status_icons[new_status]);

        // save status to library
        let id = $(this).parent().attr('data-id');
        let url = $SCRIPT_ROOT + "/_update";
        $.ajax({
            url: url,
            dataType: "json",
            contentType: "application/json",
            method: "POST",
            data: JSON.stringify({"id": id, "status": new_status})
        });
    });

    // navigation handler
    $('a.nav-link').click(function(){ 
        let clicked = $(this).text();
        $('a.nav-link').each(function(){ $(this).removeClass("active"); });
        $(this).addClass("active");
        if ( clicked == "Bookshelf" ){
            showBookshelf();
        } else if ( clicked == "Wish List" ){
            showWishList();
        } else {
            showCatalog();
        }
    });
    function showBookshelf(){
        $('.content-listing').each(function(){
            if( $(this).attr('data-status') == '1' ){
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
    function showWishList(){
        $('.content-listing').each(function(){
            if( $(this).attr('data-status') == '2' ){
                $(this).show();
            } else {
                $(this).hide();
            }
        });  
    }
    function showCatalog(){
        $('.content-listing').each(function(){
            $(this).show();
        });
    }
    // search
    $('button[type=submit]').click(function(){
        let query = $('input[name=search]').val().toUpperCase();
        showCatalog();
        $('.content-listing').each(function(){
            if ( $(this).find('.content-listing__title').text().toUpperCase().indexOf(query) == -1 ){
                $(this).hide();
            }
        });
    });

});