let page = document.querySelector(".somdPage");
let container = document.querySelector(".SDcontainer");

if (document.querySelector(".sidebar_container")) {
  // ----사이드바 기본 설정 안 보임/
  let sidebar = document.querySelector(".sidebar_container");
  sidebar.style.display = "none";

  // ----사이드바 버튼 클릭 시
  let sidebar_button = document.querySelector(".sidebar_button");

  let BlurForSidebar = document.querySelector(".BlurForSidebar");
  BlurForSidebar.style.display = "none";
  BlurForSidebar.addEventListener("click", function (event) {
    sidebar.style.display = "none";
    BlurForSidebar.style.display = "none";
  });

  sidebar_button.addEventListener("click", function (event) {
    sidebar.style.display = "flex";
    BlurForSidebar.style.display = "block";
  });

  let sidebar_button_close = document.querySelector(".sidebar_button_close");
  sidebar_button_close.addEventListener("click", function (event) {
    sidebar.style.display = "none";
    BlurForSidebar.style.display = "none";
  });

  // ----헤더 스크롤 관리
  let header = document.querySelector(".header");
  let EmptyForHeader = document.querySelector(".EmptyForHeader");

  let maxScroll = page.scrollHeight - container.clientHeight;

  let preScroll = page.scrollTop;
  let prepreScroll = page.scrollTop;
  let nowScroll = page.scrollTop;

  let headerState = "add";
  page.addEventListener("scroll", function (event) {
    maxScroll = page.scrollHeight - container.clientHeight;
    // console.log("scroll!");
    nowScroll = page.scrollTop;
    // header.innerText = maxScroll +" / " +preScroll +" -> "+nowScroll+" = "+(preScroll - nowScroll) + headerState;
    // console.log(maxScroll)
    // console.log(maxScroll +"/" +preScroll +"->"+nowScroll+"="+(preScroll - nowScroll) + headerState);
    if (maxScroll > 2) {
      if (prepreScroll != nowScroll) {
        if (nowScroll < -1) {
          // console.log("add");
          header.classList.add("add");
          header.classList.remove("remove");
          headerState = "top";
          EmptyForHeader.classList.add("addEmpty");
          EmptyForHeader.classList.remove("removeEmpty");
        } else if (nowScroll > maxScroll + 1) {
          header.classList.remove("add");
          header.classList.add("remove");
          headerState = "bottom";
          EmptyForHeader.classList.remove("addEmpty");
          EmptyForHeader.classList.add("removeEmpty");
        } else {
          if (
            preScroll - nowScroll > 5 &&
            (headerState != "bottom" ||
              (nowScroll <= maxScroll && headerState == "bottom"))
          ) {
            // console.log("add");
            header.classList.add("add");
            header.classList.remove("remove");
            headerState = "add";
            EmptyForHeader.classList.add("addEmpty");
            EmptyForHeader.classList.remove("removeEmpty");
          } else if (
            preScroll - nowScroll < -5 &&
            (headerState != "top" || (nowScroll >= 0 && headerState == "top"))
          ) {
            // console.log("remove");
            header.classList.remove("add");
            header.classList.add("remove");
            headerState = "remove";
            EmptyForHeader.classList.remove("addEmpty");
            EmptyForHeader.classList.add("removeEmpty");
          }
        }
      }
    }
    prepreScroll = preScroll;
    preScroll = nowScroll;
  });
  //

  var nowlink = document
    .querySelector(".mainTitle")
    .querySelector("div").innerText;

  if (nowlink == "메인페이지") {
    // console.log(document.querySelector(".mainpageIcon"));
    document.querySelector(".mainpageIcon").style.color = "#282828";
  } else if (nowlink == "솜디게시판") {
    document.querySelector(".boardIcon").style.color = "#282828";
  } else if (nowlink == "나의솜디") {
    document.querySelector(".mysomdIcon").style.color = "#282828";
  } else {
    document.querySelector(".navbar").style.display = "none";
  }

  var historyBack = document.querySelector(".historyBack");
  if (historyBack != null) {
    historyBack.addEventListener("click", function (event) {
      if (
        event.target == historyBack ||
        event.target.parentNode == historyBack
      ) {
        window.history.go(-1);
      }
    });
  }
}
