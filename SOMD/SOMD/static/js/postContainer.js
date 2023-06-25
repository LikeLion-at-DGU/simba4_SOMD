if(document.querySelector('.postContainer_control')){

const postContainer_control = document.querySelector('.postContainer_control');
const postContainer_control_list = postContainer_control.querySelector('.fa-list');
const postContainer_control_feed = postContainer_control.querySelector('.fa-image');


let postContainer_control_state = "리스트";
postContainer_control_feed.style.color = "lightgrey";
// console.log("dd" + postContainer_control);

postContainer_control.addEventListener('click', function(event){
    if(event.target == postContainer_control ||event.target  == postContainer_control_list || event.target == postContainer_control_feed){
        // console.log(event.target);
        let postContainer = document.querySelector(".postContainer");
        let nonImages = postContainer.getElementsByClassName("nonimage");
        // console.log(nonImages)
        if(postContainer_control_state == "리스트"){
            postContainer_control_state = "피드";
            postContainer_control_feed.style.color = "grey";
            postContainer_control_list.style.color = "lightgrey";
            postContainer.className = "postContainer album_post"
            // postContainer_control_icon.className = "fa-solid fa-list";

            for(image of nonImages){
                image.parentNode.parentNode.style.display = "none";
            }
        }
        else if (postContainer_control_state == "피드"){
            postContainer_control_state = "리스트"
            postContainer_control_list.style.color = "grey";
            postContainer_control_feed.style.color = "lightgrey";
            postContainer.className = "postContainer linebyline_post";
            
            // postContainer_control_icon.className = "fa-solid fa-image";

            for(image of nonImages){
                image.parentNode.parentNode.style.display = "block";
            }
        }
        
        // console.log(postContainer_control_state);
    }
});

}  
