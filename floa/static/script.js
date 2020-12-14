"use strict";
$(document).ready(function(){
    var $SCRIPT_ROOT = location.origin;

    // initialize home view
    var activePage = $('.nav-link active').text()
    if ( activePage = "Bookshelf" ){
        $('.content-listing').each(function(){
            if( $(this).attr('data-status') = '1' ){
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    } 
    // initialize checkbox status
    // default class is fa-circle-o
    $( '.content-listing' ).each(function(){
        if ($(this).attr('data-status') == '1'){
            $(this).find('i.fa').removeClass('fa-circle-o').addClass('fa-check');
        } else if ($(this).attr('data-status') == '2'){
            $(this).find('i.fa').removeClass('fa-circle-o').addClass('fa-heart');
        }
    });

    // tri-state checkbox click handler
    $( '.content-listing__checkbox' ).click(function(e){
        if ( $(this).parent().parent().attr('data-status') == '0' ){
            $(this).children().removeClass('fa-circle-o').addClass('fa-check');
            $(this).parent().parent().attr('data-status', '1');
        } else if ( $(this).parent().parent().attr('data-status') == '1' ){
            $(this).children().removeClass('fa-check').addClass('fa-heart');
            $(this).parent().parent().attr('data-status', '2');
        } else if ( $(this).parent().parent().attr('data-status') == '2' ){
            $(this).children().removeClass('fa-heart').addClass('fa-circle-o');
            $(this).parent().parent().attr('data-status', '0');
        }
        var id = $(this).parent().parent().attr('data-id');
        var status = $(this).parent().parent().attr('data-status');
        var url = $SCRIPT_ROOT + "/_update";
        $.ajax({
            url: url,
            dataType: "json",
            contentType: "application/json",
            method: "POST",
            data: JSON.stringify({"id": id, "status": status})
        });
    });

    // navigation handler
    $('a.nav-link').click(function(){ 
        var clicked = $(this).text();
        $('a.nav-link').each(function(){ $(this).removeClass("active"); });
        $(this).addClass("active");
        if ( clicked == "Bookshelf" ){
            $('.content-listing').each(function(){
                if( $(this).attr('data-status') = '1' ){
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        } else if ( clicked == "Wish List" ){
            $('.content-listing').each(function(){
                if( $(this).attr('data-status') = '2' ){
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });  
        } else {
            $('.content-listing').each(function(){
                $(this).show();
            });  
        }
    });
    /* search
    $('button[type=submit]').click(function(){
        var query = $('input[name=search]').val();
    });
    */

});