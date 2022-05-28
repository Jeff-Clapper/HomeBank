var valuePlaceHolder = 3

var goalModule =  `
<div class="modules goal">
    <h3 class="goal-name">Goal Name</h3>
    <h3 class="goal-objective">$20,000</h3>
    <h5 class="goal-data goal-account">Emergency Fund</h5>
    <div class="progress-container">
        <div class="progress">
            <div class="progress-bar" role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
        </div>
    </div>
    <h5 class="goal-data goal-date">5/23/2024</h5>
    <h5 class="goal-data goal-suggested-contribution">$250.00/month</h5>
</div>`

function moduleClickAction(){
    $(".goal").on("click",function(){
        $(this).css("background-color","#f7f9fa50");
        $(this).css("border-right","solid #dee1e5 1px");
        $(this).css("border-bottom","solid #dee1e5 1px");
        $(this).css("box-shadow","none");
    })
}

function moduleButtonAction(){
    $(".goal").hover(function(){
        $(this).css("background-color","#f7f9fa85");
        moduleClickAction();
    },function(){
        $(this).removeAttr("style");
        $(".goal").off();
        moduleButtonAction();
    })
}

$(document).ready(function(){
    for(i=0;i<valuePlaceHolder;i++){
        $('.add-goal').before(goalModule)
    };
    moduleButtonAction();
})