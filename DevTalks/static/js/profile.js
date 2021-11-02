(function ($) {
    'use strict';
    /*==================================================================
        [ Daterangepicker ]*/
    try {
        $('.js-datepicker').daterangepicker({
            "singleDatePicker": true,
            "showDropdowns": true,
            "autoUpdateInput": false,
            locale: {
                format: 'DD/MM/YYYY'
            },
        });
    
        var myCalendar = $('.js-datepicker');
        var isClick = 0;
    
        $(window).on('click',function(){
            isClick = 0;
            // console.log("1");
        });
    
        $(myCalendar).on('apply.daterangepicker',function(ev, picker){
            isClick = 0;
            $(this).val(picker.startDate.format('DD/MM/YYYY'));
            // console.log("2");
            calculateAge();
            console.log("Called calculateAge() Function");
        });
    
        $('.js-btn-calendar').on('click',function(e){
            e.stopPropagation();
    
            if(isClick === 1) isClick = 0;
            else if(isClick === 0) isClick = 1;
    
            if (isClick === 1) {
                myCalendar.focus();
            }
            // console.log("3");
        });
    
        $(myCalendar).on('click',function(e){
            e.stopPropagation();
            isClick = 1;
            // console.log("4");
        });
    
        $('.daterangepicker').on('click',function(e){
            e.stopPropagation();
        });
    
    
    } catch(er) {console.log(er);}
    /*[ Select 2 Config ]
        ===========================================================*/
    
    try {
        var selectSimple = $('.js-select-simple');
    
        selectSimple.each(function () {
            var that = $(this);
            var selectBox = that.find('select');
            var selectDropdown = that.find('.select-dropdown');
            selectBox.select2({
                dropdownParent: selectDropdown
            });
        });
    
    } catch (err) {
        console.log(err);
    }
    
    // $('.badge').bind("contextmenu",function(e){
    //     return false;
    // });

    $('.btn-change-profile').click(function() {
        $('#profilepicture').click();
    });

    $('#birthdate').change(function() {
        calculateAge();
    });

    function calculateAge() {
        // let format = "%d/%m/%Y";
        let dob = $("#birthdate").val().split("/");
        dob = new Date(parseInt(dob[2]), parseInt(dob[1])-1, parseInt(dob[0]));
        // console.log(dob);
        var today = new Date();
        let dayDiff = Math.ceil(today - dob) / (1000 * 60 * 60 * 24 * 365);
        var age = parseInt(dayDiff);
        // console.log(age);
        if(age>1)
            $('#age').val(age+ " Years")
        else
            $('#age').val(age+ " Year")
    }

})(jQuery);