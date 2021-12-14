// I NEED TO EDIT THIS FUNCTION TO REMOVE THE PREVIOUS DATA FROM THE LIST
// ALSO, ADDED HIDDEN TO ID TO HIDE
// ALSO, CREATE EDIT BUTTON TO EDIT THE PROM
// ALSO, CONSIDER HIDE OBTION TO HIDE OR OBSURE THE VALUE SO ONLY CURRENT USER CAN SEE THE ACTUAL NAME?


// //  // // SPECIAL NOTE!!!! CORRECT CREDIT CARDS TO SHOW NEG AND RED

function populate_transaction(){
    $(".transaction_body").html("")
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
    .done(function(results) {
        if(results.length > 0){
            for(var ind = 0; ind < results.length; ind++){
                if(results[ind].amount < 0){
                    $(".transaction_body").append(`<tr><td class="trans_id">${results[ind].id}</td><td class="trans_date">${results[ind].date}</td><td class='trans_name'>${results[ind].name}</td><td class="trans_amount negative">$${results[ind].amount}</td><td class='trans_category'>${results[ind].category}</td><td class='status'>${results[ind].pending}</td><td class='account_name'>${results[ind].account_name}</td></tr>`);    
                }
                else{
                    $(".transaction_body").append(`<tr><td class="trans_id">${results[ind].id}</td><td class="trans_date">${results[ind].date}</td><td class='trans_name'>${results[ind].name}</td><td class="trans_amount positive">$${results[ind].amount}</td><td class='trans_category'>${results[ind].category}</td><td class='status'>${results[ind].pending}</td><td class='account_name'>${results[ind].account_name}</td></tr>`);    
                }
            }
        }
        else{
            $(".transaction_body").append(`<tr><td class="trans_id"></td><td class="trans_date"></td><td class='trans_name'></td><td class="trans_amount"></td><td class='trans_category'></td><td class='status'></td><td class='account_name'></td></tr>`);    
        }
    })
}

$(document).ready(function(){
    $(".datepicker").datepicker();
    $(".accounts").selectmenu();
    populate_transaction();

    $("form").on("submit", function(event){
        populate_transaction();
        event.preventDefault();
    })



})