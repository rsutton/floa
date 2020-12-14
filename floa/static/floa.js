"use strict";
$(document).ready(function(){
    var $SCRIPT_ROOT = location.origin;
    // initialize checkboxes
    $('.content-listing__checkbox').each(function(){
        if ($(this).attr("data-status") == "1"){
            $(this).removeClass("not-have").addClass("have");
            $(this).children().removeClass('fa-circle-o').addClass('fa-check');
        } else if ($(this).attr("data-status") == "2"){
            $(this).removeClass("not-have").addClass("want");
            $(this).children().removeClass('fa-circle-o').addClass('fa-heart');
        }
    });
    $('.content-listing__checkbox').click(function(e){
        if ($(this).hasClass('not-have')){
            $(this).removeClass('not-have').addClass('have');
            $(this).children().removeClass('fa-circle-o').addClass('fa-check');
            $(this).attr('data-status', "1");
        } else if ($(this).hasClass('have')){
            $(this).removeClass('have').addClass('want');
            $(this).children().removeClass('fa-check').addClass('fa-heart');
            $(this).attr('data-status', "2");
        } else if ($(this).hasClass('want')){
            $(this).removeClass('want').addClass('not-have');
            $(this).children().removeClass('fa-heart').addClass('fa-circle-o');
            $(this).attr('data-status', "0");
        }
        var id = $(this).attr("data-id");
        var status = $(this).attr("data-status");
        var url = $SCRIPT_ROOT + "/_update";
        $.ajax({
            url: url,
            dataType: "json",
            contentType: "application/json",
            method: "POST",
            data: JSON.stringify({"id": id, "status": status})
        });
    });
    $('.content-listing__button').click(function(){
        var id = $(this).attr('data-id');
        var url = $SCRIPT_ROOT + "/_update";
        $.ajax({
            url: url,
            dataType: "json",
            contentType: "application/json",
            method: "POST",
            data: JSON.stringify({"id": id, "status": 0}),
            success: function(){location.reload()}
        });
    });
    /*
    $('button[type=submit]').click(function(){
        var query = $('input[name=search]').val();
    });
    */ 
});