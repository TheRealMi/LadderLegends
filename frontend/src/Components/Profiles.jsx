import React from "react";

function Profiles() {
  return <div id="profile">{Item()}</div>;
}

function Item() {
  return (
    <div class="flex">
      <div class="item">
        <img src="" alt="" />
        <div class="info">
          <h3>Name</h3>
          <span>Organization</span>
        </div>
      </div>
      <div class="item">
        <span>Score</span>
      </div>
    </div>
  );
}

export default Profiles;
