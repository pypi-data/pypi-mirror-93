GregorianMonth = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]


today = new Date();
clickedDay = today;
var year = today.getFullYear()
var month = today.getMonth()+1
editeID = 0;
userArray=[]


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function prev_month(){
    month -= 1;
    if(month ==0 ){
        month = 12;
        year -= 1;
    }
    getMonth();
}

function next_month(){
    month += 1;
    if(month ==13 ){
        month = 1;
        year += 1;
    }
    getMonth();
}

function getMonth(){
     $.ajax({
        url: '/getGregorianMonth/' + year + "/" + month,
        success: function(data) {
            var result = JSON.parse(data);
            events = result['events'];
            result = result['cal'];
            var tbody = document.createElement('tbody')
            tbody.setAttribute('id','myTbody')
            for(var i = 0; i<result.length; i++){
                var tr = document.createElement('tr');
                for(var j = 0; j< result[i].length; j++){
                    var td = document.createElement('td')
                    var anchor = document.createElement('a')
                    anchor.setAttribute('onClick','addEvent(this)')
                    if(result[i][j] != 0) {
                        var t = document.createTextNode(result[i][j]);
                        anchor.appendChild(t);
                        td.appendChild(anchor);
                        if(checkToday(result[i][j])){
                            td.setAttribute("style", "border:solid blue");;
                        }
                    }
                    tr.appendChild(td)
                }
                tbody.appendChild(tr)
            }
            $('#myTbody').replaceWith(tbody)
            $('#YearMonth h2').html(GregorianMonth[month-1])
            $('#YearMonth h3').html(year)
              names= []
              contents= []
              days= []
              ids= []
              ev_users= []
             for (eve in events){
                names.push(events[eve].name)
                contents.push(events[eve].content)
                days.push(events[eve].day)
                ids.push(events[eve].id)
                ev_users.push(events[eve].users)
            }
            loadEvents()
        }
     })
}


function checkToday(day){
    if(year == today.getFullYear()
        && (month-1) == today.getMonth()
        && day == today.getDate()){
        return true
    }
    return false
}


function addEvent(event){
    clickedDay = event.innerHTML.trim()
    $("#addEventDiv").attr("style","display:block")
}


function hidePlus(){
    $("#addEventAndEvent").attr("style","display:block")
    $("#eventPlus").attr("style","display:none")
}


function submitEvent(){
    if(editeID != 0){
        editEvent();
        editeID = 0;
    }
    else{
        result = evalInputs();
        if(result == true){
            $.ajax({
                url: '/addEvent/'+$('#eventName').val()+'/'+$('#eventContent').val()+'/'+year+'/'+month+"/"+clickedDay+'/'+userArray.toString(),
                type: "GET",
                success: function(returneddata) {
                    closeDiv()
                    getMonth()
                }
            })
        }
        else{
            $("#warning").attr("style","display:block")
         }
    }
}

function closeDiv(){
    $("#addEventAndEvent").attr("style","display:none")
    $("#eventPlus").attr("style","display:block")
    $("#addEventDiv").attr("style","display:none")
    $("#showEvent").html("")
    $("#eventName").val('')
    $("#eventContent").val('')
    $(".user").prop('checked', false);
    userArray=[];
    $("#warning").attr("style","display:none")
}



function evalInputs(){
    if($("#eventName").val().trim()==""){
        return false;}
    if($("#eventContent").val().trim()==""){
        return false;}
    if(userArray.length==0){
        return false;}
    return true
}
function showEvent(i){
    $("#showEvent").html("")
    for (k in days){
        temp = []
        temp2=[]
        try {
          temp = ev_users[k].split(',')
            for (e in temp){
                temp2.push(temp[e].replace(/[^a-zA-Z ]/g, "").trim())
            }
        }
        catch(err) {
          temp2=ev_users[k]
        }
        let showEventHTML = `
            <div id=`+ids[k]+`>
                <h3>`+names[k]+`</h3>
                <p>`+contents[k]+`</p>
                <p>User(s):</b> `+temp2+`</p>
                <div>
                    <a onclick="showEdite(this)">Edit</a>
                    <a onclick="deleteEvent(this)">Delete</a>
                </div>
             </div>
        `

        if(days[k]==i){
            $("#showEvent").append(showEventHTML)
        }
    }
    $("#showEvent").attr("style","display:block")
}



function loadEvents(){
    $('#myTbody').children('tr').each(function () {
        $(this).children('td').each(function (){
            j = $(this)
            let date = $(this).children('a').text().trim()
            for(let k in days){
                if (date == days[k]){
                    j.css("background-color","lightblue")
                    j.first().click(function(){
                        showEvent(days[k]);
                    })
                    break;
                }
            }
         })
    });

}


$( document ).ready(function() {
    loadEvents()
});


function showEdite(e){
    $("#addEventAndEvent").attr("style","display:block")
    $("#eventPlus").attr("style","display:none")
    id = e.parentElement.parentElement.getAttribute('id')
    for (i in ids){
        if(ids[i]==id){
            $("#eventName").val(names[i])
            $("#eventContent").val(contents[i])
            temp = ev_users[i].toString().split(',')
            counter = 0
            all_count = 0
            for(j in temp){
                all_count = 0
                temp2 = temp[j].replace(/[^a-zA-Z ]/g, "").trim()
                $(".user").each(function(k, obj) {
                    all_count++
                    if(temp2==$(this).val()){
                    $(this).prop('checked', true);
                    counter++
                    }
                });
              }
              if(counter==all_count-1){
                    $('.user').prop('checked', true);
              }
            editeID = ids[i];
            break;
        }
    }
}

function editEvent(){
    $(".user").each(function(i, obj) {
        if(obj.checked){
            userArray.push(obj.value)
            }
    });
    result = evalInputs();
    if(result == true){
        $.ajax({
            url: '/editeEvent/'+$('#eventName').val()+'/'+$('#eventContent').val()+'/'+year+'/'+month+"/"+clickedDay+"/"+editeID+'/'+userArray.toString(),
            type: "GET",
            success: function(returneddata) {
                closeDiv()
                getMonth()
            }
        })

    }
    else{
        $("#warning").attr("style","display:block")
     }
}


function deleteEvent(e){
    $.ajax({
        url: '/deleteEvent/'+e.parentElement.parentElement.getAttribute('id'),
        type: "GET",
        success: function(returneddata) {
            closeDiv()
            getMonth()
        }
    })
}



function addUser(user){
    userArray=[]
    if(user.value=='all'){
        if(user.checked){
            $(".user").prop('checked', true);
        }
        else{
            $(".user").prop('checked', false);
        }
    }
    else{
        if(!user.checked){
            $("#all").prop('checked', false)
        }
        else{
            numItems = $('.user').length-1
            numberOfChecked = $('.user:checked').length;
            if(numberOfChecked==numItems){
                $("#all").prop('checked', true)
            }
        }
    }
    $(".user").each(function(i, obj) {
        if(obj.checked)
            userArray.push(obj.value)
    });
}

