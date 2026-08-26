console.log("JavaScript is running");

fetch("kpi_data.json")
.then(response => response.json())
.then(data => {

    document.getElementById("total-apps").innerText =
        data.total_apps.toLocaleString();

    document.getElementById("total-installs").innerText =
        data.total_installs.toLocaleString();
        
    document.getElementById("avg-rating").innerText =
        data.avg_rating;
        
    document.getElementById("total-reviews").innerText =
        data.total_reviews.toLocaleString();    
});

function animateValue(id, start,end,duration){
    let obj = document.getElementById(id);
    let range = end - start;
    let current = start;
    let increment = range / (duration / 20);
    let timer = setInterval(function(){
        current += increment;
        if(current >= end){
            current = end;
            clearInterval(timer);

        }

        if(end < 10){
            obj.innerHTML=current.toFixed(2);

        }

        else{
            obj.innerHTML=Math.floor(current).toLocaleString();
        }

    },20);
}

window.onload=function(){
    animateValue("total-apps",0,10841,1800);
    animateValue("total-installs",0,15432000000,2000);
    animateValue("avg-rating",0,4.19,1800);
    animateValue("total-reviews",0,781652300,2000);
}

function updateDateTime(){
    const now = new Date();

    document.getElementById("current-date").innerHTML =
    today.toLocaleString("en-IN",
     {
        weekday: "short",
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
    });

    document.getElementById("current-date").innerHTML =
        now.toLocaleString("en-IN", options);
}

window.addEventListener("load",function(){
    const loader=document.getElementById("loader");

    setTimeout(function(){

        loader.style.opacity="0";

        loader.style.transition="0.5s";

        setTimeout(function(){

            loader.style.display="none";

        },500);
    },1200);
});



fetch("filter_data.json")
    .then(response => response.json())
    .then(data => {


        const category = document.getElementById("category-filter");
        const month = document.getElementById("month-filter");

        

        data.categories.forEach(function (item) {
            const option = document.createElement("option");

            option.value = item;
            option.textContent = item;

            category.appendChild(option);

        });

        data.months.forEach(function (item) {
            const option = document.createElement("option");

            option.value = item;
            option.textContent = item;

            month.appendChild(option);
        });

        console.log("category and Month filters loaded successfully");

    })
    .catch(error => {
        console.error("Error loading filter_data.json:", error );
    });


let data=[];

const cat = document.getElementById("category-filter");
const mon = document.getElementById("month-filter");
const rat = document.getElementById("rating-filter");

fetch("dashboard_data.json")
.then(r=> r.json())
.then(d=> {
    data = d;
    
    update();
});

function update() {
    let x = data.filter(a=>
    (cat.value === "All" || a.category === cat.value)&&
    (mon.value === "All" || a.month === mon.value) &&
    (rat.value === "All" || Number(a.rating) >= Number(rat.value))
    );

    let ratings = x
         .map(a => Number(a.rating))
         .filter(a => !isNaN(a))

    document.getElementById("total-apps").innerText =
        x.length.toLocaleString();

    document.getElementById("total-installs").innerText =
        x.reduce((s,a) => s + (Number(a.installs) ||0),0).toLocaleString();

    document.getElementById("total-reviews").innerText =
        x.reduce((s,a) => s + (Number(a.reviews) || 0), 0).toLocaleString();

    document.getElementById("avg-rating").innerText =
        ratings.length ? (ratings.reduce((a,b) => a+b, 0) / ratings.length).toFixed(2) : "0.00";

}

[cat,mon,rat].forEach(x => x.addEventListener("change", function()
{
    update();
    sendFiltersToCharts();
})
);

function sendFiltersToCharts() {

    const filters = {
        category: cat.value,
        month: mon.value,
        rating: rat.value
    };

    const charts = [
        "Task1-chart",
        "Task2-chart",
        "Task3-chart",
        "Task4-chart",
        "Task5-chart",
        "Task6-chart"
    ];

    charts.forEach(function(id){

        const iframe = document.getElementById(id);
        if (iframe && iframe.contentWindow) {
            iframe.contentWindow.postMessage(
                { 
                    type: "dashboardFilters",
                    filters: filters
                },
                "*"    
            );
        }
     });
}