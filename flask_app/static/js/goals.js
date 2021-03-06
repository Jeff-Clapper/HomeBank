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

var newGoalModal = `
<div class="new-goal-modal active-modal" id="new-goal-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-head">Create Goal</h3>
            </div>
            <form action="#" method="post">
                <div class="modal-body">
                    <div class="user_input">
                        <input type="text" class="form-control" id="name" name='name' placeholder="Name of Goal">
                    </div>
                    <div class="user_input">
                        <input type="number" class="form-control" id="goal-amount" name='goal-amount' placeholder="Goal Amount">
                    </div>
                    <div class="form-control payday-user-selector">
                        <input type="hidden" name="THIS WILL BE ACCOUNT NAME" value="{{user['ACCOUNTNAME VARIABLE HERE']}}">
                        <select name="accociated-account" class="accociated-account" id="accociated-account">
                            <option value="user">Account 1</option>
                            <option value="user">Account 2</option>
                            <option value="user">Account 3</option>
                            <option value="user">Account 4</option>
                        </select>
                    </div>
                    <div class="user_input">
                        <input type="date" class="form-control datepicker end-date" id="end-date" name='end-date' placeholder="OPTIONAL: End Date">
                    </div>
                    <div class="user_input">
                        <input type="text" class="form-control reward" id="reward" name='reward' placeholder="OPTIONAL: Reward Upon Completion">
                    </div>
                    <div class="user_input checkbox">
                        <div class="checkbox-container">
                            <input type="checkbox" class="monthly-contribution" id="monthly-contribution" name='monthly-contribution'>
                        </div>
                        <h6 class="create-goal-checkbox-text">Suggest Monthly Contribution</h6>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary close" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-secondary submit">Submit</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>`

var currGoalDetailsModal = `
<div class="existing-goal-modal active-modal" id="existing-goal-modal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-head">Goal #</h3>
            </div>
            <div class="modal-body goal-body">
                <h3 class="goal-objective goal-breakdown-data">$20,000</h3>
                <h5 class="goal-data goal-account goal-breakdown-data">Account: Emergency Fund</h5>
                <div class="progress-container goal-breakdown-data modal-progress-container">
                    <div class="progress goal-breakdown-data">
                        <div class="progress-bar" role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                </div>
                <h5 class="goal-data goal-date goal-breakdown-data">End Date: 5/23/2024</h5>
                <h5 class="goal-data goal-suggested-contribution goal-breakdown-data">Monthly Contribution: $250.00/month</h5>
                <div class='goal-breakdown-data reward-text-box'>
                    <h5 class="goal-data goal-reward">Reward:</h5>
                    <p class="">The reward for this goal will be a trip to Disney.</p>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-outline-secondary edit" data-bs-dismiss="modal">Edit</button>
                <button type="submit" class="btn btn-secondary close">Close</button>
            </div>
        </div>
    </div>
</div>`

var currGoalEditModal = `
<div class="existing-goal-modal-update active-modal" id="existing-goal-modal-updates" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-head">Goal #</h3>
            </div>
            <form action="#" method="post">
                <div class="modal-body">
                    <div class="user_input">
                        <input type="text" class="form-control" id="name" name='name' placeholder="Emergency Fund Goal">
                    </div>
                    <div class="user_input">
                        <input type="number" class="form-control" id="goal-amount" name='goal-amount' placeholder="16000">
                    </div>
                    <div class="form-control payday-user-selector">
                        <input type="hidden" name="THIS WILL BE ACCOUNT NAME" value="{{user['ACCOUNTNAME VARIABLE HERE']}}">
                        <select name="accociated-account" class="accociated-account" id="accociated-account">
                            <option value="user">Account 1</option>
                            <option value="user">Account 2</option>
                            <option value="user">Account 3</option>
                            <option value="user">Account 4</option>
                        </select>
                    </div>
                    <div class="user_input">
                        <input type="date" class="form-control datepicker end-date" id="end-date" name='end-date'>
                    </div>
                    <div class="user_input">
                        <input type="text" class="form-control reward" id="reward" name='reward' placeholder="We will go to Disney">
                    </div>
                    <div class="user_input checkbox">
                        <div class="checkbox-container">
                            <input type="checkbox" class="monthly-contribution" id="monthly-contribution" name='monthly-contribution'>
                        </div>
                        <h6 class="create-goal-checkbox-text">Suggest Monthly Contribution</h6>
                    </div>
                    <div class="user_input checkbox">
                        <div class="checkbox-container">
                            <input type="checkbox" class="close-out-goal" id="close-out-goal" name='close-out-goal'>
                        </div>
                        <h6 class="close-out-goal-checkbox-text">Close Out Goal</h6>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary cancel" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-secondary submit">Submit</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>`

var overlay = '<div id="overlay"></div>'

var progressBarStats = `
    <div class="progress-bar-stats">
        <p class="percentage">75%</p>
        <p class="current-goal-funds">$15,000</p>
    </div>` 

    var valuePlaceHolder = 3

function moduleClickAction(){
    $(".goal").on("click",function(){
        activateModal(this);
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

function activateModal(module){
    addOverlay();
    if($(module).is(".add-goal")){
        $(".goals-modules-area").after(newGoalModal)
    }
    else{
        $(".goals-modules-area").after(currGoalDetailsModal);
        progressbarPercentageHoverActivation();
        $(".edit").on("click",function(){
            $(".active-modal").remove();
            $(".goals-modules-area").after(currGoalEditModal);
            $(".cancel").on("click",function(){
                $(".active-modal").remove();
                $(".goals-modules-area").after(currGoalDetailsModal);
                activateCloseButton();
            })
        })
    };
    activateCloseButton();
}

function activateCloseButton(){
    $(".close").on("click",function(){
        closeModal();
    })
}

function progressbarPercentageHoverActivation() {
    $(".progress").hover(function(event){
        // THE COMMENTED OUT SECTION DID NOT WORK, IT WOULD HAVE WORKED ON ANYTHING NOT MY MODAL. I AM KEEPING THIS FOR FUTURE STUDY
        // var xCoord = event.pageX;
        // var yCoord = event.pageY;
        // var modalCoords = $(".active-modal").offset()
        // xCoord -= modalCoords.left
        // yCoord -= modalCoords.top
        // // console.log("modal-top: ",modalCoords.top)
        // // console.log("modal-left: ",modalCoords.left)
        // console.log("xCoord: ",xCoord)
        // console.log("yCoord: ",yCoord)
        $(".modal-progress-container").after(progressBarStats);
        $(".progress-bar-stats").css("top","35%");
        $(".progress-bar-stats").css("left","95%");
    }, function() {
        $(".progress-bar-stats").remove();
    })
}

function closeModal(){
    $(".active-modal").remove();
    $("#overlay").remove();
}

function addOverlay(){
    $("#transaction-base").before(overlay);
    $("#overlay").on("click",function(){
        closeModal();
    })
}

$(document).ready(function(){
    for(i=0;i<valuePlaceHolder;i++){
        $('.add-goal').before(goalModule)
    };
    moduleButtonAction();
})

