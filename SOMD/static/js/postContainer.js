if(document.querySelector('.postContainer_control')){

const postContainer_control = document.querySelector('.postContainer_control');
const postContainer_control_list = postContainer_control.querySelector('.fa-list');
const postContainer_control_feed = postContainer_control.querySelector('.fa-image');


var notice_container = `
    <i class="fa-solid fa-circle-exclamation"></i> 
    피드형에서는 사진이 첨부된 게시글만 볼 수 있어요
`
let postContainer_control_state = "리스트";
postContainer_control_feed.style.color = "lightgrey";
// console.log("dd" + postContainer_control);

let admin_linebyline = document.getElementsByClassName("admin_linebyline")
let admin_album = document.getElementsByClassName("admin_album")
let Post_image;
let fixedPost_image;
let notice = document.getElementById("container_notice")
// console.log(Post_image)
// console.log(fixedPost_image)

postContainer_control.addEventListener('click', function(event){
    if(event.target == postContainer_control ||event.target  == postContainer_control_list || event.target == postContainer_control_feed){
        // console.log(event.target);
        let postContainer = document.querySelector(".postContainer");
        let nonImages = postContainer.getElementsByClassName("nonimage");
        // console.log(nonImages)

        //피드
        if(postContainer_control_state == "리스트"){
            postContainer_control_state = "피드";
            postContainer_control_feed.style.color = "grey";
            postContainer_control_list.style.color = "lightgrey";
            postContainer.className = "postContainer album_post"


            if(document.querySelector("#Post_image") !=null){
                Post_image = document.querySelector("#Post_image");
                Post_image.className ="album_post warning"
                Post_image.style.display = "flex";
            }
            
            if(document.querySelector("#fixedPost_image")!=null ){
                fixedPost_image = document.querySelector("#fixedPost_image");
                fixedPost_image.className ="album_post warning"
                fixedPost_image.style.display= "flex";
            }

            // postContainer_control_icon.className = "fa-solid fa-list";

            for(image of nonImages){
                image.parentNode.parentNode.style.display = "none";
            }

            for(admin of admin_album){
                admin.style.display = "block";
            }
            for(admin of admin_linebyline){
                admin.style.display = "none";
            }
            notice.innerHTML = notice_container;
        }

        // 리스트
        else if (postContainer_control_state == "피드"){
            postContainer_control_state = "리스트"
            postContainer_control_list.style.color = "grey";
            postContainer_control_feed.style.color = "lightgrey";
            postContainer.className = "postContainer linebyline_post";
            
            // postContainer_control_icon.className = "fa-solid fa-image";


            if(document.querySelector("#Post_image") !=null){
                Post_image = document.querySelector("#Post_image");
                Post_image.className ="linebyline_post warning"
                Post_image.style.display ="none";
            }
            
            if(document.querySelector("#fixedPost_image")!=null ){
                fixedPost_image = document.querySelector("#fixedPost_image");
                fixedPost_image.className ="linebyline_post warning"
                fixedPost_image.style.display="none";
            }


            for(image of nonImages){
                image.parentNode.parentNode.style.display = "block";
            }
            for(admin of admin_album){
                admin.style.display = "none";
            }

            for(admin of admin_linebyline){
                admin.style.display = "block";
            }
            notice.innerHTML = ""
        }
        // console.log(postContainer_control_state);
    }
});

}  
