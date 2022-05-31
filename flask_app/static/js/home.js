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

// NOTES FOR LATER:
// when inserting the modules, I will be using the jQuery ".append()" 
// accountModule gets appended to .home-page-accounts
// goalModule gets appened to .goals
// personPaydayModule gets appended to .module-column-right

$(document).ready(function(){

})