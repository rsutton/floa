"use strict";
$(document).ready(function(){
    const $SCRIPT_ROOT = location.origin;
    const view_labels = ["Catalog", "Bookshelf", "Wish List", "Updates"];
    const status_icons = ["fa-circle-o", "fa-check", "fa-heart", "fa-star"];

    // initialize home view
    filterList("Bookshelf");

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
    });

    // navigation handler
    $('a.nav-link').click(function(){
        clearSearch();
        let clicked = $(this).text();
        $('a.nav-link').each(function(){ $(this).removeClass("active"); });
        $(this).addClass("active");
        filterList(clicked);
    });

    function filterList(clicked){
        if ( clicked == "Updates" ){
            let url = $SCRIPT_ROOT + "/_update/catalog";
            $.ajax({
                url: url,
                // TODO new updates are not populating until after a page reload...
                success: function(){
                    $('a.nav-link').each(function(){ $(this).removeClass("active"); });
                    $("a.nav-link:contains('Updates')").addClass("active");
                }
            });
        }
        let status = $.inArray(clicked, view_labels);
        $('.content-listing').each(function(){
            if( clicked == "Catalog" || $(this).attr('data-status') == status ){
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }

    // searchbox
    function clearSearch(){
        $('input[name=search]').val('');
    }

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