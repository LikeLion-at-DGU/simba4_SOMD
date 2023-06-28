let page_main = document.querySelector(".somdPage");
let page_header = document.querySelector(".somdPage_header");
let somdList = document.querySelector(".somdList");
let all_somdList = document.querySelector(".all_somdList");
let option = document.querySelector(".option");
let title = document.querySelector(".mainTitle")
let EmptyForTitle = document.querySelector(".EmptyForTitle")
let Scroll = page_main.scrollTop;
// console.log("연결");

let boader_state ="add";
page_main.addEventListener('scroll', function(event){
    Scroll  = page_main.scrollTop;
    if(Scroll>160){
        somdList.style.display = "none";
        title.style.display ="none";
        EmptyForTitle.style.height = "150px";
        page_header.appendChild(option);
        boader_state ="remove";
    }
    else if(Scroll < 90){
        boader_state = "add";
        // page_main.scrollTop = 2;
        if(boader_state == "add" && Scroll < 2){
            EmptyForTitle.style.height = "0px";
            somdList.style.display = "block";
            title.style.display ="flex";
            // EmptyForTitle.style.height = "0px";
            page_main.insertBefore(option,all_somdList);
        }
        else{
            page_main.scrollTop = 145;
        }
    }

    //  console.log(option.parentNode);
    // console.log(boader_state);
    // console.log(Scroll);
});
// 


