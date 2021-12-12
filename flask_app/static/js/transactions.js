// WANT TO MAKE A FUNCTION, CALL THE FUNCTION ON OPEN USING "ALL" AND START/END BLANK
// NEED TO APPEND OR ADD HTML UNIT FOR EACH VALUE RETURNED

$(document).ready(function(){
    $(".datepicker").datepicker();
    $(".accounts").selectmenu();
    
    $("form").on("submit", function(event){
        var data_url = "/user/"+user_id+"/get_transactions"
        
        var test = {
            family_id: $('input[name="family_id"]').val(),
            account: $('select[name="account"]').val(),
            start_date: $('input[name="start_date"]').val(),
            end_date: $('input[name="end_date"]').val()
        }
        console.log(test)

        $.ajax({
            data : {
                family_id: $('input[name="family_id"]').val(),
                account_id: $('select[name="account"]').val(),
                start_date: $('input[name="start_date"]').val(),
                end_date: $('input[name="end_date"]').val()
            },
            type: "POST",
            url: data_url
        })
        .done(function(data) {
            console.log(data)
        })
        event.preventDefault();

    })



})