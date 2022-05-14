// I NEED TO EDIT THIS FUNCTION TO REMOVE THE PREVIOUS DATA FROM THE LIST



// //  // // SPECIAL NOTE!!!! CORRECT CREDIT CARDS TO SHOW NEG AND RED

var monthlyProfitModule =  `
<div class="modules monthly-profit-module">
    <h3 class=module-header>Profits By Month</h3>
    <div class="monthly-profit-graph-image">
        <img src="C:\\Users\\Jeff Clapper\\OneDrive - Clap Nation\\Desktop\\test\\HomeBank\\flask_app\\static\\images\\bar-graph.png" width="80%" height="202">
    </div>
</div>`


var accountPropertiesModule = `
<div class="modules monthly-profit-module">
    <h3 class=module-header>Bank of America Checking Properties</h3>
    <div class="account-properties">
        <h5 class="property nickname"> Nickname: Emergancy Fund</h5>
        <h5 class="property purpose"> Purpose: Emergancy Fund</h5>
        <h5 class="property type"> Account Type: Checking</h5>
        <h5 class="property bank"> Bank Name: Bank of America</h5>
        <h5 class="property curr-balance"> Current Balance: $12,202.84</h5>
        <h5 class="property pending"> Pending Charges: $1,112.41</h5>
    </div>
</div>`


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
                    $(".transaction_body").append(`<tr><td class="trans_id" hidden>${results[ind].id}</td><td class="trans_date">${results[ind].date}</td><td class='trans_name'>${results[ind].name}</td><td class="trans_amount negative">$${results[ind].amount}</td><td class='trans_category'>${results[ind].category}</td><td class='status'>${results[ind].pending}</td><td class='account_name'>${results[ind].account_name}</td></tr>`);    
                }
                else{
                    $(".transaction_body").append(`<tr><td class="trans_id" hidden>${results[ind].id}</td><td class="trans_date">${results[ind].date}</td><td class='trans_name'>${results[ind].name}</td><td class="trans_amount positive">$${results[ind].amount}</td><td class='trans_category'>${results[ind].category}</td><td class='status'>${results[ind].pending}</td><td class='account_name'>${results[ind].account_name}</td></tr>`);    
                }
            }
        }
        else{
            $(".transaction_body").append(`<tr><td class="trans_id"></td><td class="trans_date"></td><td class='trans_name'></td><td class="trans_amount"></td><td class='trans_category'></td><td class='status'></td><td class='account_name'></td></tr>`);    
        }
    })
}

function attachAccountToggleClickListener() {
    $(".btn-outline-secondary").on("click", function() {
        var toBeUnselected = $(".selected")
        toggleFromButton(toBeUnselected)
        toggleToButton(this)
    })
}

function setMiddleModuleToGraph(){
    $(".module-column-middle").html(monthlyProfitModule);
}

function setMiddleModuleToAccountProperties (toButton) {
    // This will need to be adjusted to account for which account is being selected
    $(".module-column-middle").html(accountPropertiesModule);
}

function toggleToButton(toButton) {
    $(toButton).removeClass("btn-outline-secondary");
    $(toButton).addClass("btn-secondary");
    $(toButton).addClass("selected");
    if($(toButton).is(".all-accounts")) {
        setMiddleModuleToGraph();
    } else if ($(toButton).is(".obscured")) {
        $(".module-column-middle").html("")
    } else {
        console.log("entering ELSE")
        setMiddleModuleToAccountProperties(toButton);
    }
} 

function toggleFromButton(toBeUnselected) {
    $(toBeUnselected).removeClass("btn-secondary");
    $(toBeUnselected).removeClass("selected");
    $(toBeUnselected).addClass("btn-outline-secondary");
    attachAccountToggleClickListener();
}

$(document).ready(function(){
    // This next line will be changed once we incorporate routing to include an if statement
    setMiddleModuleToGraph();
    attachAccountToggleClickListener();
    $(".datepicker").datepicker();
    $(".accounts").selectmenu();
    // populate_transaction();

    // $("form").on("submit", function(event){
    //     populate_transaction();
    //     event.preventDefault();
    // })
})