var accountModule = `
<div class="account">
    <h4 class="account-name">Account Name</h4>
    <h3  class="available-funds">$1906.24</h3>
    <p>opt: Purpose</p>
</div>`

var goalModule = `
<div class="goal">
    <h4 class="goal-name">Goal Name</h4>
    <div class="progress-container">
        <div class="progress">
            <div class="progress-bar" role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
    </div>
</div>`

var personPaydayModule = `
<div class="modules person">
    <h4 class="person-header">Abigail's<br>Next Payday</h4>
    <h3 class="person-paydate">5/1/2022</h3>
    <h5 class="person-header">Est: $1354.54</h5>
</div>`

var goalPlaceHolder = 6
var accountPlaceHolder = 7
var personPlaceHolder = 2

function populateAccounts(){
    for(var i = 0; i < accountPlaceHolder; i++){
        $(".home-page-accounts").append(accountModule)
    };
    accountHoverActivation();
}

function populateGoals(){
    for(var i = 0; i < goalPlaceHolder; i++){
        $(".goals").append(goalModule)
    };
    goalHoverActivation()
}

function populatePaydays(){
    for(var i = 0; i < personPlaceHolder; i++){
        $(".module-column-right").append(personPaydayModule)
    };
    paydayHoverActivation();
}

function hoverAction(module){
    $(module).css("border", "3px solid #6e388a59");
}

function accountHoverActivation(){
    $(".account").hover(function(){
        hoverAction(this);
        $(this).css("padding","3px 9px")
        $(this).on("click",function(){
            console.log("This will link to the accounts page, specifically this account")
        })
    },
    function(){
        $(this).removeAttr("style");
        $(".account").off();
        accountHoverActivation();
    });
}

function paydayHoverActivation(){
    $(".person").hover(function(){
        hoverAction(this);
        $(this).css("padding","17px");
        $(this).on("click",function(){
            console.log("this will link to the payday of this specific person")
        });
    },
    function(){
        $(this).removeAttr("style");
        $(".person").off();
        paydayHoverActivation();
    });
    }

function goalHoverActivation(){
    $(".goals-data").hover(function(){
        hoverAction(this);
        $(this).css("padding","17px");
        $(this).on("click",function(){
            console.log("This will link to the goals for this family")
        })
    },function(){
        $(this).removeAttr("style");
        $(".goals-data").off();
        goalHoverActivation();
    })
}

function toButtonActivation(){
    $('.to-button').on("click",function(){
        var linkTo = $(this).attr("to");
        console.log("this button is working. Going to ",linkTo);
    })
}

$(document).ready(function(){
    populateAccounts();
    populateGoals();
    populatePaydays();
    toButtonActivation();
})