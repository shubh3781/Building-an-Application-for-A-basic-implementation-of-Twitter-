var countF = 0;
var countButton = document.getElementById("followButton");
var displayCount = document.getElementById("followers");
countButton.onclick = function() {
if (countButton.innerText == "Follow") {
    countF++;
    countButton.innerText = "Unfollow";
  } else if (countButton.innerText == "Unfollow") {
    countF--;
    countButton.innerText = "Follow";
  }
}