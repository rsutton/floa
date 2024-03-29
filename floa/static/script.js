"use strict";
var counter = 0;
const $SCRIPT_ROOT = location.origin;
const view_labels = ["Catalog", "Bookshelf", "Wish List", "New"];
const status_icons = ["fa-circle-o", "fa-check", "fa-heart", "fa-star", "fa-warning"];

$(document).ready(function(){

    // show bookshelf and update icons
    $( '.content-listing' ).each(function(){
        let status = $(this).attr('data-status')
        $(this).children('.content-listing__control').removeClass(iconClassMatcher).addClass(status_icons[status]);
    });
    showView("Bookshelf");

    // handle checkbox status
    function iconClassMatcher(index, className){
        let matchedClasses = className.match(/(^|\s)fa-\S+/g)
        return (matchedClasses || []).join('')
    }
    // multi-state checkbox click handler
    $( '.content-listing__control' ).click(function(){
        let current_status = parseInt($(this).parent().attr('data-status'));
        let new_status = (current_status + 1) % status_icons.length;
        $(this).parent().attr('data-status', new_status);
        $(this).removeClass(iconClassMatcher).addClass(status_icons[new_status]);

        // save status to library
        let id = $(this).parent().attr('data-id');
        let url = $SCRIPT_ROOT + "/_update/item";
        $.ajax({
            url: url,
            dataType: "json",
            contentType: "application/json",
            method: "POST",
            data: JSON.stringify({"id": id, "status": new_status})
        });
        update_bookshelf_counter();
    });

    // navigation handler
    $('a.nav__link').click(function(){
        clearSearch();
        let clicked = $(this).text();
        showView(clicked)
    });

    // searchbox
    function clearSearch(){
        $('input[name=search]').val('');
    }

    $('button[type=submit]').click(function(e){
        e.preventDefault();
        let query = $('input[name=search]').val().toUpperCase();
        showView('Catalog');
        $('.content-listing').each(function(){
            if ( $(this).find('.content-listing__title').text().toUpperCase().indexOf(query) == -1 ){
                $(this).hide();
            }
        });
    });

    // view controllers
    function showView(view){
        let counter = update_bookshelf_counter();
        $('a.nav__link').each(function(){ $(this).removeClass("active"); });
        $('a.nav__link:contains("' + view + '")').addClass("active");
        filterList(view);
        if ( view === "Help" || ( view === "Bookshelf" && counter == 0 )){
                $('.help').show();
                $('.content-list').hide();
                $('.message').hide();
        }
        else {
            $('.help').hide();
            $('.content-list').show();
            $('.message').show();
        }
    }
    function filterList(clicked){
        let status = $.inArray(clicked, view_labels);
        $('.content-listing').each(function(){
            if( clicked === "Catalog" || $(this).attr('data-status') == status ){
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
    function update_bookshelf_counter(){
        counter = 0;
        $( '.content-listing' ).each(function(){
            if ( $(this).attr('data-status') == '1' ){
                counter = counter + 1;
            }
        });
        $( '.counter' ).text(counter);
        return counter;
    }

});