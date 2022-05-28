// On load, this block will generat to the planned tab. When the actual tab is selected, it will go through and change the class to btn-secondary, the headers of the column to actual, and the data to match the actual money transfered
var previousPlannedModule = `
<div class="modules previous-paydays">
    <div class="previous-header">
        <h3 class="module-header">Previous 3</h3>
        <div class="planned-actual-toggle-buttons">
            <div class="payday-previous-toggle-button">
                <button type="submit" class="btn btn-secondary selected planned">Planned</button>
            </div>
            <div class="payday-previous-toggle-button">
                <button type="submit" class="btn btn-outline-secondary not-selected actual">Actual</button>
            </div>
            <div class="payday-previous-toggle-button">
                <button type="submit" class="btn btn-outline-secondary not-selected OTHERPERSONNAMEHERE">Jeffery</button>
            </div>
        </div>
    </div>
    <div class="previous-tables"></div>
</div>`

// The below html block will go into .previous-tables in .previous-paydays in .module-column-lower
var previousPlannedTables = `
<div class="previous-table-area">
    <h4 class="previous-date">August 26th, 2022</h4>
    <table class="table payday-table previous-table">
        <thead class="thead-hb-theme"> 
            <tr>
                <th scope="col" class='th-account-name-column'>Planned</th>

                <!-- This will need to be pulled from previous data (maybe previous paychecks) -->
                
                <th scope="col" class='th-funds-column'>$1364.24</th>
            </tr>
        </thead>
        <tbody class="payday-body"></tbody>

        <!-- This will be a for loop -->
        <!-- This will require User input and may need to be an api call, or I may need to have the frontend do math -->
            
            <tr>
                <td class='td-name-column account-name'>Account 1</td>
                <td class='td-money-column account-name-funds'>$801.13</td>
            </tr>
        <!-- endfor -->
        </tbody>
    </table>
</div>`

var otherUsersPlannedActualModule = `
<div class="modules payday">
    <div class="previous-header">
        <h2 class="paydate-person module-header">Jeffery's Last Planned Paycheck</h2>
        <div class="planned-actual-toggle-buttons">
            <div class="payday-previous-toggle-button">
                <button type="submit" class="btn btn-outline-secondary not-selected planned">Planned</button>
            </div>
            <div class="payday-previous-toggle-button">
                <button type="submit" class="btn btn-outline-secondary not-selected actual">Actual</button>
            </div>
            <div class="payday-previous-toggle-button">
                <button type="submit" class="btn btn-secondary selected OTHERPERSONNAMEHERE">Jeffery</button>
            </div>
        </div>
    </div>
    <div class="current-payday-tables">
        <div class="current-payday-table">
            <table class="table payday-table planned-table">
                <thead class="thead-hb-theme"> 
                    <tr>
                        <th scope="col" class='th-account-name-column'>Planned</th>

                        <!-- This will need to be pulled from previous data (maybe previous paychecks) -->

                        <th scope="col" class='th-funds-column planned-funds'>$1364.24</th>
                    </tr>
                </thead>
                <tbody class="payday-body"></tbody>

                <!-- This will be a for loop -->
                <!-- This will require User input and may need to be an api call, or I may need to have the frontend do math -->
                
                    <tr>
                        <td class='td-name-column account-name'>Account 1</td>
                        <td class='td-money-column account-name-funds'>$801.13</td>
                    </tr>

                <!-- endfor -->
                </tbody>
            </table>
        </div>
        <div class="current-payday-table">
            <table class="table payday-table actual-table">
                <thead class="thead-hb-theme"> 
                    <tr>
                        <th scope="col" class='th-account-name-column'>Actual</th>
                        <!-- this will need to be pulled from the bank account -->
                        <th scope="col" class='th-funds-column actual-funds'>$1364.24</th>
                    </tr>
                </thead>
                <tbody class="payday-body"></tbody>
                <!-- This will be a for loop -->
                <!-- This will require User input and may need to be an api call, or I may need to have the frontend do math -->
                    <tr>
                        <td class='td-name-column account-name'>Account 1</td>
                        <td class='td-money-column account-name-funds'>$801.13</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>`

function clearBottomModule() {
    $('.module-column-lower').children().remove();
    $('.module-column-lower').html(previousPlannedModule);
}

function setBottomModuleToPlanned() {
    clearBottomModule();
    for(ind=0;ind<3;ind++){
        $('.previous-tables').append(previousPlannedTables);
        // This section will be used to populate the data (OR I can create a new function that will populate the data)
    };
    attachAccountToggleClickListener();
}

function setBottomModuleToActual() {
    setBottomModuleToPlanned();
    var toBeUnselected = $(".selected");
    toggleFromButton(toBeUnselected);
    toggleToButton(".actual");
    $(".previous-table .th-account-name-column").text("Actual");
    attachAccountToggleClickListener()

}

function setBottomModuleToOtherUser() {
    $(".module-column-lower").html(otherUsersPlannedActualModule);
    attachAccountToggleClickListener();
}

function attachAccountToggleClickListener(){
    $(".not-selected").off();
    $(".not-selected").on("click", function(){
        var unselected = $(".selected");
        toggleFromButton(unselected);
        toggleToButton(this);
        setBottomModule();
    })
}

function toggleToButton(toButton){
    $(toButton).removeClass("btn-outline-secondary");
    $(toButton).removeClass("not-selected")
    $(toButton).addClass("btn-secondary");
    $(toButton).addClass("selected");
}

function toggleFromButton(toBeUnselected) {
    $(toBeUnselected).removeClass("btn-secondary");
    $(toBeUnselected).removeClass("selected");
    $(toBeUnselected).addClass("btn-outline-secondary");
    $(toBeUnselected).addClass("not-selected")
    // attachAccountToggleClickListener();
}

function setBottomModule() {
    if($(".selected").is(".planned")) {
        setBottomModuleToPlanned()
    }
    else if ($(".selected").is(".actual")) {
        setBottomModuleToActual()
    }
    else {
        setBottomModuleToOtherUser()
    }
}

$(document).ready(function(){
    $('.module-column-lower').html(previousPlannedModule);
    setBottomModuleToPlanned();

});